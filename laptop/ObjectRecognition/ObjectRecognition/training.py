# -*- coding: utf-8 -*-

import cv2
import sys
import zmq
import base64
import numpy as np
import tkinter as tk
from tkinter import messagebox  # import this to fix messagebox error
from PIL import Image


def mkdir(path):
    # 引入模块
    import os

    path = path.strip()
    path = path.rstrip("\\")

    # Determine whether the path exists
    isExists = os.path.exists(path)

    # critical result
    if not isExists:
        # Create a directory if it does not exist
        os.makedirs(path)

        print
        path + ' 创建成功'
        return True
    else:
        # If the directory exists, do not create it, and prompt that the directory already exists
        print
        path + ' 目录已存在'
        return False

def CatchPICFromVideo(catch_pic_num, path_name):
    context = zmq.Context()
    footage_socket = context.socket(zmq.PAIR)
    footage_socket.bind('tcp://*:5555')


    classfier = cv2.CascadeClassifier("D:/software/Anaconda/pkgs/libopencv-3.4.2-h20b85fd_0/Library/etc/haarcascades/haarcascade_frontalface_alt2.xml")

    color = (0, 255, 0)

    num = 0

    mkdir(path_name)

    while True:
        print("listion")
        frame = footage_socket.recv_string()
        img = base64.b64decode(frame)
        npimg = np.frombuffer(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)

        grey = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)

        # Face detection, 1.2 and 2 are the image zoom ratio and the effective number of points to be detected respectively
        faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(faceRects) > 0:  # If greater than 0, a face is detected
            for faceRect in faceRects:  # Frame each face individually
                x, y, w, h = faceRect

                # Save the current frame as a picture
                img_name = '%s/%d.jpg' % (path_name, num)
                print(img_name)
                image = source[y - 10: y + h + 10, x - 10: x + w + 10]
                cv2.imwrite(img_name, image)

                num += 1
                if num > (catch_pic_num):  # Exit the loop if it exceeds the specified maximum number of saves
                    break

                # Draw a rectangle
                cv2.rectangle(source, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)

                # Shows how many face pictures have been captured so far
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(source, 'num:%d' % (num), (x + 30, y + 30), font, 1, (255, 0, 255), 4)

        # End the program beyond the specified maximum save quantity
        if num > (catch_pic_num): break

        # Display image
        cv2.imshow('Recording', source)
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break
    # Release the camera and destroy all windows
    cv2.destroyAllWindows()
    situation = open('D:/ObjectRecognition/translate/PC_Command.txt', 'w')
    situation.write('0')
    situation.close()
    tk.messagebox.showinfo('That\'s all', 'Record is over.')


if __name__ == '__main__':
    CatchPICFromVideo(100, 'D:/ObjectRecognition/data/lee')
