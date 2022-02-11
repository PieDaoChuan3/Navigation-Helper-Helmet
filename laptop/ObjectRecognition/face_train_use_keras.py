#-*- coding: utf-8 -*-
import random

import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from keras.models import load_model
from keras import backend as K

from load_face_dataset import load_dataset, resize_image, IMAGE_SIZE

class Dataset:
    def __init__(self, path_name):
        # Training set
        self.train_images = None
        self.train_labels = None

        # Validation set
        self.valid_images = None
        self.valid_labels = None

        # Test set
        self.test_images  = None
        self.test_labels  = None

        # Data set loading path
        self.path_name    = path_name

        self.input_shape = None

    # Load the data set and divide the data set according to the principle of cross-validation and perform related preprocessing work
    def load(self, nb_classes, img_rows = IMAGE_SIZE, img_cols = IMAGE_SIZE,
             img_channels = 3):
        # Load data set into memory
        images, labels = load_dataset(self.path_name)

        train_images, valid_images, train_labels, valid_labels = train_test_split(images, labels, test_size = 0.3, random_state = random.randint(0, 100))
        _, test_images, _, test_labels = train_test_split(images, labels, test_size = 0.5, random_state = random.randint(0, 100))

        # This part of the code is to reorganize the training data set according to the dimension order required by the keras library
        if K.image_dim_ordering() == 'th':
            train_images = train_images.reshape(train_images.shape[0], img_channels, img_rows, img_cols)
            valid_images = valid_images.reshape(valid_images.shape[0], img_channels, img_rows, img_cols)
            test_images = test_images.reshape(test_images.shape[0], img_channels, img_rows, img_cols)
            self.input_shape = (img_channels, img_rows, img_cols)
        else:
            train_images = train_images.reshape(train_images.shape[0], img_rows, img_cols, img_channels)
            valid_images = valid_images.reshape(valid_images.shape[0], img_rows, img_cols, img_channels)
            test_images = test_images.reshape(test_images.shape[0], img_rows, img_cols, img_channels)
            self.input_shape = (img_rows, img_cols, img_channels)

            # Output the number of training set, validation set, and test set
            print(train_images.shape[0], 'train samples')
            print(valid_images.shape[0], 'valid samples')
            print(test_images.shape[0], 'test samples')

            #Our model uses 'categorical_crossentropy' as the loss function, so it needs to be based on the number of categories 'nb_classes'
            #Category label is vectorized by one-hot encoding. Here we have only two categories. After conversion, the label data becomes two-dimensional
            train_labels = np_utils.to_categorical(train_labels, nb_classes)
            valid_labels = np_utils.to_categorical(valid_labels, nb_classes)
            test_labels = np_utils.to_categorical(test_labels, nb_classes)

            # Pixel data is floated for normalization
            train_images = train_images.astype('float32')
            valid_images = valid_images.astype('float32')
            test_images = test_images.astype('float32')

            # Normalize it, and the pixel value of the image is normalized to the interval of 0~1
            train_images /= 255
            valid_images /= 255
            test_images /= 255

            self.train_images = train_images
            self.valid_images = valid_images
            self.test_images  = test_images
            self.train_labels = train_labels
            self.valid_labels = valid_labels
            self.test_labels  = test_labels

        # CNN网络模型类

class Model:
   def __init__(self):
        self.model = None

        # Bulid model
   def build_model(self, nb_classes, dataset):
            # Construct an empty network model, it is a linear stack model,
            # each neural network layer will be added sequentially, the professional name is sequential model or linear stack model
        self.model = Sequential()

            # The following code will sequentially add the layers required by the CNN network, an add is a network layer
        self.model.add(Convolution2D(32, 3, 3, border_mode='same',
                                         input_shape=dataset.input_shape))
        self.model.add(Activation('relu'))

        self.model.add(Convolution2D(32, 3, 3))
        self.model.add(Activation('relu'))

        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        self.model.add(Convolution2D(64, 3, 3, border_mode='same'))
        self.model.add(Activation('relu'))

        self.model.add(Convolution2D(64, 3, 3))
        self.model.add(Activation('relu'))

        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        self.model.add(Flatten())
        self.model.add(Dense(512))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(nb_classes))
        self.model.add(Activation('softmax'))

            # Output model overview
        self.model.summary()
            # Training model
   MODEL_PATH = './me.face.model.h5'
   def save_model(self, file_path=MODEL_PATH):
       self.model.save(file_path)
   def load_model(self, file_path=MODEL_PATH):
       self.model = load_model(file_path)

   def face_predict(self, image):
        if K.image_dim_ordering() == 'th' and image.shape != (1, 3, IMAGE_SIZE, IMAGE_SIZE):
               image = resize_image(image)  # The size must be consistent with the training set, and it should be IMAGE_SIZE x IMAGE_SIZE
               image = image.reshape((1, 3, IMAGE_SIZE, IMAGE_SIZE))
        elif K.image_dim_ordering() == 'tf' and image.shape != (1, IMAGE_SIZE, IMAGE_SIZE, 3):
               image = resize_image(image)
               image = image.reshape((1, IMAGE_SIZE, IMAGE_SIZE, 3))

           # Floating point and normalization
        image = image.astype('float32')
        image /= 255
        result = self.model.predict_proba(image)
        print('result:', result)
           # Give category prediction: 0 or 1
        result = self.model.predict_classes(image)
        return result[0]

   def train(self, dataset, batch_size, nb_epoch , data_augmentation = True):
        sgd = SGD(lr = 0.01, decay = 1e-6,
                  momentum = 0.9, nesterov = True) # Use the optimizer of SGD+momentum for training, first generate an optimizer object
        self.model.compile(loss='categorical_crossentropy',
                           optimizer=sgd,
                           metrics=['accuracy'])


        if not data_augmentation:
            self.model.fit(dataset.train_images,
                           dataset.train_labels,
                           batch_size = batch_size,
                           nb_epoch = nb_epoch,
                           validation_data = (dataset.valid_images, dataset.valid_labels),
                           shuffle = True)
        else:
            # Define a data generator for data promotion, which returns a generator object datagen, one for each datagen called
            # Secondly, it generates a set of data (sequential generation) to save memory. In fact, it is the data generator of python
            datagen = ImageDataGenerator(
                featurewise_center = False,             # Whether to decentralize the input data (mean value is 0)
                samplewise_center  = False,             # Whether to make the mean of each sample of the input data 0
                featurewise_std_normalization = False,  # Whether the data is standardized (input data divided by the
                                                        # standard deviation of the data set)
                samplewise_std_normalization  = False,  # Whether to divide each sample data by its own standard
                                                        # deviation
                zca_whitening = False,                  # Whether to apply ZCA whitening to the input data
                rotation_range = 20,                    # The angle at which the image rotates randomly when the data
                                                        # is increased (range 0～180)
                width_shift_range  = 0.2,               # The magnitude of the horizontal offset of the picture when
                # the data is promoted (unit is the proportion of the picture width, a floating point number between
                                                        # 0 and 1)
                height_shift_range = 0.2,               # Same as above, but here is vertical
                horizontal_flip = True,                 # Whether to perform random horizontal flip
                vertical_flip = False)                  # Whether to perform random vertical flip

            # Calculate the number of the entire training sample set for eigenvalue normalization, ZCA whitening, etc.
            datagen.fit(dataset.train_images)

            # Use the generator to start training the model
            self.model.fit_generator(datagen.flow(dataset.train_images, dataset.train_labels,
                                                   batch_size = batch_size),
                                     samples_per_epoch = dataset.train_images.shape[0],
                                     nb_epoch = nb_epoch,
                                     validation_data = (dataset.valid_images, dataset.valid_labels))


if __name__ == '__main__':
    dataset = Dataset('./data/')
    # nb_classes=the number of person you want to train+unknown
    dataset.load(nb_classes = 4)
    # batch_size and nb_epoch would effect the accuracy and time of training model
    batch_size = 75
    nb_epoch = 150
    model = Model()
    model.build_model(dataset, nb_classes = 4)
    model.train(dataset, batch_size, nb_epoch)
    # where model is
    model.save_model(file_path = 'D:/ObjectRecognition/model/me.face.model.h5')