"""Miscellaneous utility functions."""

import numpy as np
import keras
import keras.backend as K
from functools import reduce
from PIL import Image
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
import cv2
def compose(*funcs):
    if funcs:
        return reduce(lambda f, g: lambda *a, **kw: g(f(*a, **kw)), funcs)
    else:
        raise ValueError('Composition of empty sequence not supported.')

def letterbox_image(image, size):
    iw, ih = image.size
    w, h = size
    scale = min(w/iw, h/ih)
    nw = int(iw*scale)
    nh = int(ih*scale)

    image = image.resize((nw,nh), Image.BICUBIC)
    new_image = Image.new('RGB', size, (128,128,128))
    new_image.paste(image, ((w-nw)//2, (h-nh)//2))
    return new_image

def rand(a=0, b=1):
    return np.random.rand()*(b-a) + a

def merge_bboxes(bboxes, cutx, cuty):
    merge_bbox = []
    for i in range(len(bboxes)):
        for box in bboxes[i]:
            tmp_box = []
            x1,y1,x2,y2 = box[0], box[1], box[2], box[3]

            if i == 0:
                if y1 > cuty or x1 > cutx:
                    continue
                if y2 >= cuty and y1 <= cuty:
                    y2 = cuty
                    if y2-y1 < 5:
                        continue
                if x2 >= cutx and x1 <= cutx:
                    x2 = cutx
                    if x2-x1 < 5:
                        continue
                
            if i == 1:
                if y2 < cuty or x1 > cutx:
                    continue

                if y2 >= cuty and y1 <= cuty:
                    y1 = cuty
                    if y2-y1 < 5:
                        continue
                
                if x2 >= cutx and x1 <= cutx:
                    x2 = cutx
                    if x2-x1 < 5:
                        continue

            if i == 2:
                if y2 < cuty or x2 < cutx:
                    continue

                if y2 >= cuty and y1 <= cuty:
                    y1 = cuty
                    if y2-y1 < 5:
                        continue

                if x2 >= cutx and x1 <= cutx:
                    x1 = cutx
                    if x2-x1 < 5:
                        continue

            if i == 3:
                if y1 > cuty or x2 < cutx:
                    continue

                if y2 >= cuty and y1 <= cuty:
                    y2 = cuty
                    if y2-y1 < 5:
                        continue

                if x2 >= cutx and x1 <= cutx:
                    x1 = cutx
                    if x2-x1 < 5:
                        continue

            tmp_box.append(x1)
            tmp_box.append(y1)
            tmp_box.append(x2)
            tmp_box.append(y2)
            tmp_box.append(box[-1])
            merge_bbox.append(tmp_box)
    return merge_bbox

def get_random_data_with_Mosaic(annotation_line, input_shape, max_boxes=100, hue=.1, sat=1.5, val=1.5):
    '''random preprocessing for real-time data augmentation'''
    h, w = input_shape
    min_offset_x = 0.4
    min_offset_y = 0.4
    scale_low = 1-min(min_offset_x,min_offset_y)
    scale_high = scale_low+0.2

    image_datas = [] 
    box_datas = []
    index = 0

    place_x = [0,0,int(w*min_offset_x),int(w*min_offset_x)]
    place_y = [0,int(h*min_offset_y),int(h*min_offset_y),0]
    for line in annotation_line:
        # Split each line
        line_content = line.split()
        # Open picture
        image = Image.open(line_content[0])
        image = image.convert("RGB") 
        # The size of the picture
        iw, ih = image.size
        # Save box location
        box = np.array([np.array(list(map(int,box.split(',')))) for box in line_content[1:]])
        
        # Whether to flip the picture
        flip = rand()<.5
        if flip and len(box)>0:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            box[:, [0,2]] = iw - box[:, [2,0]]

        # Zoom in and zoom out the input image
        new_ar = w/h
        scale = rand(scale_low, scale_high)
        if new_ar < 1:
            nh = int(scale*h)
            nw = int(nh*new_ar)
        else:
            nw = int(scale*w)
            nh = int(nw/new_ar)
        image = image.resize((nw,nh), Image.BICUBIC)

        # Perform color gamut conversion
        hue = rand(-hue, hue)
        sat = rand(1, sat) if rand()<.5 else 1/rand(1, sat)
        val = rand(1, val) if rand()<.5 else 1/rand(1, val)
        x = cv2.cvtColor(np.array(image,np.float32)/255, cv2.COLOR_RGB2HSV)
        x[..., 0] += hue*360
        x[..., 0][x[..., 0]>1] -= 1
        x[..., 0][x[..., 0]<0] += 1
        x[..., 1] *= sat
        x[..., 2] *= val
        x[x[:,:, 0]>360, 0] = 360
        x[:, :, 1:][x[:, :, 1:]>1] = 1
        x[x<0] = 0
        image = cv2.cvtColor(x, cv2.COLOR_HSV2RGB) # numpy array, 0 to 1

        image = Image.fromarray((image*255).astype(np.uint8))
        # Place the pictures to correspond to the positions of the four divided pictures
        dx = place_x[index]
        dy = place_y[index]
        new_image = Image.new('RGB', (w,h), (128,128,128))
        new_image.paste(image, (dx, dy))
        image_data = np.array(new_image)/255

        
        index = index + 1
        box_data = []
        # Reprocess the box
        if len(box)>0:
            np.random.shuffle(box)
            box[:, [0,2]] = box[:, [0,2]]*nw/iw + dx
            box[:, [1,3]] = box[:, [1,3]]*nh/ih + dy
            box[:, 0:2][box[:, 0:2]<0] = 0
            box[:, 2][box[:, 2]>w] = w
            box[:, 3][box[:, 3]>h] = h
            box_w = box[:, 2] - box[:, 0]
            box_h = box[:, 3] - box[:, 1]
            box = box[np.logical_and(box_w>1, box_h>1)]
            box_data = np.zeros((len(box),5))
            box_data[:len(box)] = box
        
        image_datas.append(image_data)
        box_datas.append(box_data)

    # Split the picture and put it together
    cutx = np.random.randint(int(w*min_offset_x), int(w*(1 - min_offset_x)))
    cuty = np.random.randint(int(h*min_offset_y), int(h*(1 - min_offset_y)))

    new_image = np.zeros([h,w,3])
    new_image[:cuty, :cutx, :] = image_datas[0][:cuty, :cutx, :]
    new_image[cuty:, :cutx, :] = image_datas[1][cuty:, :cutx, :]
    new_image[cuty:, cutx:, :] = image_datas[2][cuty:, cutx:, :]
    new_image[:cuty, cutx:, :] = image_datas[3][:cuty, cutx:, :]

    # Further processing the frame
    new_boxes = merge_bboxes(box_datas, cutx, cuty)

    # Adjust the box
    box_data = np.zeros((max_boxes,5))
    if len(new_boxes)>0:
        if len(new_boxes)>max_boxes: new_boxes = new_boxes[:max_boxes]
        box_data[:len(new_boxes)] = new_boxes
    return new_image, box_data


def get_random_data(annotation_line, input_shape, max_boxes=100, jitter=.3, hue=.1, sat=1.5, val=1.5):
    '''random preprocessing for real-time data augmentation'''
    line = annotation_line.split()
    image = Image.open(line[0])
    iw, ih = image.size
    h, w = input_shape
    box = np.array([np.array(list(map(float, box.split(',')))) for box in line[1:]])

    # Scale the image and distort the length and width
    new_ar = w/h * rand(1-jitter,1+jitter)/rand(1-jitter,1+jitter)
    scale = rand(.25,2)
    if new_ar < 1:
        nh = int(scale*h)
        nw = int(nh*new_ar)
    else:
        nw = int(scale*w)
        nh = int(nw/new_ar)
    image = image.resize((nw,nh), Image.BICUBIC)

    # Add gray bars to the extra part of the image
    dx = int(rand(0, w-nw))
    dy = int(rand(0, h-nh))
    new_image = Image.new('RGB', (w,h), (128,128,128))
    new_image.paste(image, (dx, dy))
    image = new_image

    # Flip image
    flip = rand()<.5
    if flip: image = image.transpose(Image.FLIP_LEFT_RIGHT)

    # Color gamut distortion
    hue = rand(-hue, hue)
    sat = rand(1, sat) if rand()<.5 else 1/rand(1, sat)
    val = rand(1, val) if rand()<.5 else 1/rand(1, val)
    x = cv2.cvtColor(np.array(image,np.float32)/255, cv2.COLOR_RGB2HSV)
    x[..., 0] += hue*360
    x[..., 0][x[..., 0]>1] -= 1
    x[..., 0][x[..., 0]<0] += 1
    x[..., 1] *= sat
    x[..., 2] *= val
    x[x[:,:, 0]>360, 0] = 360
    x[:, :, 1:][x[:, :, 1:]>1] = 1
    x[x<0] = 0
    image_data = cv2.cvtColor(x, cv2.COLOR_HSV2RGB) # numpy array, 0 to 1

    # Adjust the box
    box_data = np.zeros((max_boxes,5))
    if len(box)>0:
        np.random.shuffle(box)
        box[:, [0,2]] = box[:, [0,2]]*nw/iw + dx
        box[:, [1,3]] = box[:, [1,3]]*nh/ih + dy
        if flip: box[:, [0,2]] = w - box[:, [2,0]]
        box[:, 0:2][box[:, 0:2]<0] = 0
        box[:, 2][box[:, 2]>w] = w
        box[:, 3][box[:, 3]>h] = h
        box_w = box[:, 2] - box[:, 0]
        box_h = box[:, 3] - box[:, 1]
        box = box[np.logical_and(box_w>1, box_h>1)] # discard invalid box
        if len(box)>max_boxes: box = box[:max_boxes]
        box_data[:len(box)] = box
    
    return image_data, box_data


def cosine_decay_with_warmup(global_step,
                             learning_rate_base,
                             total_steps,
                             warmup_learning_rate=0.0,
                             warmup_steps=0,
                             hold_base_rate_steps=0,
                             min_learn_rate=0,
                             ):
    """
    parameter???
        global_step: The Tcur defined above records the number of steps currently executed.
        learning_rate_base???The preset learning rate, when the warm_up stage learning rate increases to learning_rate_base, the learning rate starts to decrease.
        total_steps: Is the total number of training steps, equal to epoch*sample_count/batch_size, (sample_count is the total number of samples, epoch is the total number of cycles)
        warmup_learning_rate: This is the initial value of linear growth during warm up
        warmup_steps: The total number of steps required to continue warm_up
        hold_base_rate_steps: This is an optional parameter, that is, when the warm up phase is over, the learning rate is kept unchanged, and the learning rate starts to decrease after the hold_base_rate_steps is over.
    """
    if total_steps < warmup_steps:
        raise ValueError('total_steps must be larger or equal to '
                            'warmup_steps.')
    #The principle of cosine annealing is implemented here, and the
    # minimum learning rate is set to 0, so the expression is simplified
    learning_rate = 0.5 * learning_rate_base * (1 + np.cos(np.pi *
        (global_step - warmup_steps - hold_base_rate_steps) / float(total_steps - warmup_steps - hold_base_rate_steps)))
    #If hold_base_rate_steps is greater than 0, it indicates that the learning rate remains unchanged
    # within a certain number of steps after the warm up is over
    if hold_base_rate_steps > 0:
        learning_rate = np.where(global_step > warmup_steps + hold_base_rate_steps,
                                    learning_rate, learning_rate_base)
    if warmup_steps > 0:
        if learning_rate_base < warmup_learning_rate:
            raise ValueError('learning_rate_base must be larger or equal to '
                                'warmup_learning_rate.')
        # Realization of linear growth
        slope = (learning_rate_base - warmup_learning_rate) / warmup_steps
        warmup_rate = slope * global_step + warmup_learning_rate
        # Only when the global_step is still in the warm up phase, the linearly increasing learning rate warmup_rate will
        # be used, otherwise the learning rate learning_rate of cosine annealing will be used
        learning_rate = np.where(global_step < warmup_steps, warmup_rate,
                                    learning_rate)

    learning_rate = max(learning_rate,min_learn_rate)
    return learning_rate


class WarmUpCosineDecayScheduler(keras.callbacks.Callback):
    """
    Inherit the Callback to realize the scheduling of the learning rate
    """
    def __init__(self,
                 learning_rate_base,
                 total_steps,
                 global_step_init=0,
                 warmup_learning_rate=0.0,
                 warmup_steps=0,
                 hold_base_rate_steps=0,
                 min_learn_rate=0,
                 # interval_epoch represents the lowest point between cosine annealing
                 interval_epoch=[0.05, 0.15, 0.30, 0.50],
                 verbose=0):
        super(WarmUpCosineDecayScheduler, self).__init__()
        # Basic learning rate
        self.learning_rate_base = learning_rate_base
        # Thermal adjustment parameters
        self.warmup_learning_rate = warmup_learning_rate
        # Parameter display
        self.verbose = verbose
        # learning_rates is used to record the learning rate after each update to facilitate graphical observation
        self.min_learn_rate = min_learn_rate
        self.learning_rates = []

        self.interval_epoch = interval_epoch
        # Step size across the whole world
        self.global_step_for_interval = global_step_init
        # Total step length used for ascent
        self.warmup_steps_for_interval = warmup_steps
        # Keep the total step length of the highest peak
        self.hold_steps_for_interval = hold_base_rate_steps
        # The total step length of the whole training
        self.total_steps_for_interval = total_steps

        self.interval_index = 0
        # Calculate the distance between the two lowest points
        self.interval_reset = [self.interval_epoch[0]]
        for i in range(len(self.interval_epoch)-1):
            self.interval_reset.append(self.interval_epoch[i+1]-self.interval_epoch[i])
        self.interval_reset.append(1-self.interval_epoch[-1])

	#Update global_step and record the current learning rate
    def on_batch_end(self, batch, logs=None):
        self.global_step = self.global_step + 1
        self.global_step_for_interval = self.global_step_for_interval + 1
        lr = K.get_value(self.model.optimizer.lr)
        self.learning_rates.append(lr)

	#Update learning rate
    def on_batch_begin(self, batch, logs=None):
        # ??????????????????????????????????????????
        if self.global_step_for_interval in [0]+[int(i*self.total_steps_for_interval) for i in self.interval_epoch]:
            self.total_steps = self.total_steps_for_interval * self.interval_reset[self.interval_index]
            self.warmup_steps = self.warmup_steps_for_interval * self.interval_reset[self.interval_index]
            self.hold_base_rate_steps = self.hold_steps_for_interval * self.interval_reset[self.interval_index]
            self.global_step = 0
            self.interval_index += 1

        lr = cosine_decay_with_warmup(global_step=self.global_step,
                                      learning_rate_base=self.learning_rate_base,
                                      total_steps=self.total_steps,
                                      warmup_learning_rate=self.warmup_learning_rate,
                                      warmup_steps=self.warmup_steps,
                                      hold_base_rate_steps=self.hold_base_rate_steps,
                                      min_learn_rate = self.min_learn_rate)
        K.set_value(self.model.optimizer.lr, lr)
        if self.verbose > 0:
            print('\nBatch %05d: setting learning '
                  'rate to %s.' % (self.global_step + 1, lr))
