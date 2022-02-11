# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import cv2

IMAGE_SIZE = 64


# Adjust the size according to the specified image size
def resize_image(image, height=IMAGE_SIZE, width=IMAGE_SIZE):
    top, bottom, left, right = (0, 0, 0, 0)

    # Get image size
    h, w, _ = image.shape

    # For pictures with unequal length and width, find the longest side
    longest_edge = max(h, w)

    # To calculate the short side, you need to increase the pixel width to make it the same length as the long side
    if h < longest_edge:
        dh = longest_edge - h
        top = dh // 2
        bottom = dh - top
    elif w < longest_edge:
        dw = longest_edge - w
        left = dw // 2
        right = dw - left
    else:
        pass

    # RGB颜色
    BLACK = [0, 0, 0]

    # Add a border to the image, which is the length and width of the image, and cv2.BORDER_CONSTANT specifies the border color
    constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)

    # Resize the image and return
    return cv2.resize(constant, (height, width))


# Read training data
images = []
labels = []


def read_path(path_name):
    for dir_item in os.listdir(path_name):
        # Start stacking from the initial path and merge into a recognizable operation path
        full_path = os.path.abspath(os.path.join(path_name, dir_item))

        if os.path.isdir(full_path):  # If it is a folder, continue to call recursively
            read_path(full_path)
        else:
            if dir_item.endswith('.jpg'):
                image = cv2.imread(full_path)
                image = resize_image(image, IMAGE_SIZE, IMAGE_SIZE)

                # cv2.imwrite('1.jpg', image)

                images.append(image)
                labels.append(path_name)

    return images, labels


# Read training data from the specified path
def load_dataset(path_name):
    images, labels = read_path(path_name)

    # Convert all the input pictures into a four-dimensional array, the size is (number of pictures*IMAGE_SIZE*IMAGE_SIZE*3)
    # The picture is 64 * 64 pixels, one pixel has 3 color values (RGB)
    images = np.array(images)
    print(images.shape)

    # Annotate the data
    for label in range(0, len(labels)):
        if labels[label].endswith('Junlin Hai'):
            labels[label] = 0
        elif labels[label].endswith('Jingwei Yang'):
            labels[label] = 1
        elif labels[label].endswith('Bo Sun'):
            labels[label] = 2
        else:
            labels[label] = 3
    print(labels)
    return images, labels


if __name__ == '__main__':
    images, labels = load_dataset('D:/object recognition/data')
