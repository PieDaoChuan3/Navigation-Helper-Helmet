import numpy as np
import tensorflow as tf
from keras import backend as K
from nets.ious import box_ciou

#---------------------------------------------------#
#   Smooth label
#---------------------------------------------------#
def _smooth_labels(y_true, label_smoothing):
    num_classes = tf.cast(K.shape(y_true)[-1], dtype=K.floatx())
    label_smoothing = K.constant(label_smoothing, dtype=K.floatx())
    return y_true * (1.0 - label_smoothing) + label_smoothing / num_classes
#---------------------------------------------------#
#   Adjust each feature layer of the predicted value to the true value
#---------------------------------------------------#
def yolo_head(feats, anchors, num_classes, input_shape, calc_loss=False):
    num_anchors = len(anchors)
    # [1, 1, 1, num_anchors, 2]
    anchors_tensor = K.reshape(K.constant(anchors), [1, 1, 1, num_anchors, 2])

    # 获得x，y的网格
    # (13, 13, 1, 2)
    grid_shape = K.shape(feats)[1:3] # height, width
    grid_y = K.tile(K.reshape(K.arange(0, stop=grid_shape[0]), [-1, 1, 1, 1]),
        [1, grid_shape[1], 1, 1])
    grid_x = K.tile(K.reshape(K.arange(0, stop=grid_shape[1]), [1, -1, 1, 1]),
        [grid_shape[0], 1, 1, 1])
    grid = K.concatenate([grid_x, grid_y])
    grid = K.cast(grid, K.dtype(feats))

    # (batch_size,13,13,3,85)
    feats = K.reshape(feats, [-1, grid_shape[0], grid_shape[1], num_anchors, num_classes + 5])

    # Adjust the predicted value to the true value
    # box_xy corresponds to the center point of the box
    # box_wh corresponds to the width and height of the box
    box_xy = (K.sigmoid(feats[..., :2]) + grid) / K.cast(grid_shape[::-1], K.dtype(feats))
    box_wh = K.exp(feats[..., 2:4]) * anchors_tensor / K.cast(input_shape[::-1], K.dtype(feats))
    box_confidence = K.sigmoid(feats[..., 4:5])
    box_class_probs = K.sigmoid(feats[..., 5:])

    # The following parameters are returned when calculating loss
    if calc_loss == True:
        return grid, feats, box_xy, box_wh
    return box_xy, box_wh, box_confidence, box_class_probs

#---------------------------------------------------#
#   Used to calculate the iou of each predicted box and the ground truth box
#---------------------------------------------------#
def box_iou(b1, b2):
    # 13,13,3,1,4
    # Calculate the coordinates of the upper left corner and the lower right corner
    b1 = K.expand_dims(b1, -2)
    b1_xy = b1[..., :2]
    b1_wh = b1[..., 2:4]
    b1_wh_half = b1_wh/2.
    b1_mins = b1_xy - b1_wh_half
    b1_maxes = b1_xy + b1_wh_half

    # 1,n,4
    # Calculate the coordinates of the upper left and lower right corners
    b2 = K.expand_dims(b2, 0)
    b2_xy = b2[..., :2]
    b2_wh = b2[..., 2:4]
    b2_wh_half = b2_wh/2.
    b2_mins = b2_xy - b2_wh_half
    b2_maxes = b2_xy + b2_wh_half

    # Calculate the overlap area
    intersect_mins = K.maximum(b1_mins, b2_mins)
    intersect_maxes = K.minimum(b1_maxes, b2_maxes)
    intersect_wh = K.maximum(intersect_maxes - intersect_mins, 0.)
    intersect_area = intersect_wh[..., 0] * intersect_wh[..., 1]
    b1_area = b1_wh[..., 0] * b1_wh[..., 1]
    b2_area = b2_wh[..., 0] * b2_wh[..., 1]
    iou = intersect_area / (b1_area + b2_area - intersect_area)

    return iou


#---------------------------------------------------#
#   Loss value calculation
#---------------------------------------------------#
def yolo_loss(args, anchors, num_classes, ignore_thresh=.5, label_smoothing=0.1, print_loss=False):

    # There are 2 floors
    num_layers = len(anchors)//3

    # Separate the prediction result from the actual ground truth, args is [*model_body.output, *y_true]
    # y_true is a list containing two feature layers, the shapes are (m,13,13,3,85), (m,26,26,3,85)
    # yolo_outputs is a list containing two feature layers, the shapes are (m,13,13,255), (m,26,26,255)
    y_true = args[num_layers:]
    yolo_outputs = args[:num_layers]

    # A priori box
    anchor_mask = [[6,7,8], [3,4,5], [0,1,2]] if num_layers==3 else [[3,4,5], [1,2,3]]

    # Get input_shpae as 608,608
    input_shape = K.cast(K.shape(yolo_outputs[0])[1:3] * 32, K.dtype(y_true[0]))

    loss = 0

    # Take out every picture
    # The value of m is batch_size
    m = K.shape(yolo_outputs[0])[0]
    mf = K.cast(m, K.dtype(yolo_outputs[0]))

    # y_true is a list containing two feature layers, the shapes are (m,13,13,3,85), (m,26,26,3,85)
    # yolo_outputs is a list containing two feature layers, the shapes are (m,13,13,255), (m,26,26,255)
    for l in range(num_layers):
        # Take the first feature layer (m, 13, 13, 3, 85) as an example
        # The position of the point where the target exists in the feature layer is extracted. (m,13,13,3,1)
        object_mask = y_true[l][..., 4:5]
        # Take out its corresponding type (m,13,13,3,80)
        true_class_probs = y_true[l][..., 5:]
        if label_smoothing:
            true_class_probs = _smooth_labels(true_class_probs, label_smoothing)

        # Process the feature layer output of yolo_outputs
        # grid is the grid structure (13,13,1,2), raw_pred is the unprocessed prediction result (m,13,13,3,85)
        # And the decoded xy, wh, (m,13,13,3,2)
        grid, raw_pred, pred_xy, pred_wh = yolo_head(yolo_outputs[l],
             anchors[anchor_mask[l]], num_classes, input_shape, calc_loss=True)
        
        # This is the position of the predicted box after decoding
        # (m,13,13,3,4)
        pred_box = K.concatenate([pred_xy, pred_wh])

        # To find the negative sample group, the first step is to create an array, []
        ignore_mask = tf.TensorArray(K.dtype(y_true[0]), size=1, dynamic_size=True)
        object_mask_bool = K.cast(object_mask, 'bool')
        
        # Calculate ignore_mask for each picture
        def loop_body(b, ignore_mask):
            # Take out the parameters of all the boxes that actually exist in the b-th sub-picture
            # n,4
            true_box = tf.boolean_mask(y_true[l][b,...,0:4], object_mask_bool[b,...,0])
            # Calculate the iou between the predicted result and the real situation
            # pred_box is 13,13,3,4
            # The calculated result is the iou of each pred_box and all other real boxes
            # 13,13,3,n
            iou = box_iou(pred_box[b], true_box)

            # 13,13,3
            best_iou = K.max(iou, axis=-1)

            # If the degree of coincidence between some prediction boxes and the ground truth boxes is greater than 0.5, they are ignored.
            ignore_mask = ignore_mask.write(b, K.cast(best_iou<ignore_thresh, K.dtype(true_box)))
            return b+1, ignore_mask

        # Traverse all pictures
        _, ignore_mask = K.control_flow_ops.while_loop(lambda b,*args: b<m, loop_body, [0, ignore_mask])

        # Compress and process the content of each picture
        ignore_mask = ignore_mask.stack()
        #(m,13,13,3,1)
        ignore_mask = K.expand_dims(ignore_mask, -1)

        box_loss_scale = 2 - y_true[l][...,2:3]*y_true[l][...,3:4]

        # Calculate ciou loss as location loss
        raw_true_box = y_true[l][...,0:4]
        ciou = box_ciou(pred_box, raw_true_box)
        ciou_loss = object_mask * box_loss_scale * (1 - ciou)
        ciou_loss = K.sum(ciou_loss) / mf
        location_loss = ciou_loss
        
        # If there is a frame at the position, then calculate the cross entropy of 1 and the confidence
        # If there is no frame at this position, and 'best_iou<ignore_thresh' is satisfied, it is considered as a negative sample
        # 'best_iou<ignore_thresh' is used to limit the number of negative samples
        confidence_loss = object_mask * K.binary_crossentropy(object_mask, raw_pred[...,4:5], from_logits=True)+ \
            (1-object_mask) * K.binary_crossentropy(object_mask, raw_pred[...,4:5], from_logits=True) * ignore_mask
        
        class_loss = object_mask * K.binary_crossentropy(true_class_probs, raw_pred[...,5:], from_logits=True)

        confidence_loss = K.sum(confidence_loss) / mf
        class_loss = K.sum(class_loss) / mf
        loss += location_loss + confidence_loss + class_loss
        # if print_loss:
        # loss = tf.Print(loss, [loss, confidence_loss, class_loss, location_loss], message='loss: ')
    return loss
