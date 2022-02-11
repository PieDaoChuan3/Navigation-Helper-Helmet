#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cv2
import time
import zmq
import base64
import picamera
from picamera.array import PiRGBArray


def run():
  IP = '172.20.10.3:5555' #IP address of the video receiver 
  """Initialize the camera part """
  camera = picamera.PiCamera()
  camera.resolution = (640,480)
  camera.framerate = 20
  rawCapture = PiRGBArray(camera, size = (640,480))

  """Instantiate the zmq object used to send the frame """
  contest = zmq.Context()
  """zmq object uses TCP communication protocol"""
  footage_socket = contest.socket(zmq.PAIR)
  """Establish a TCP communication protocol between the zmq object and the video receiver """
  footage_socket.connect('tcp://%s'%IP)
  print(IP)

  """Collect images from the camera in a loop
     Since you are using a raspberry pie camera, you need to set use_video_port to True
     frame is the captured image """
  for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
      frame_image = frame.array #Convert the collected images to numpy array 
      encoded, buffer = cv2.imencode('.jpg', frame_image) #Convert the converted image data into stream data again ，
                                                        # And store the stream data in the internal buffer 
      jpg_as_test = base64.b64encode(buffer) #Base64 encode the image stream data in memory 
      footage_socket.send(jpg_as_test) #Send the encoded stream data to the receiving end of the video 
      rawCapture.truncate(0) #Release the memory and prepare for the next frame of video image transmission 
      time.sleep(0.1)