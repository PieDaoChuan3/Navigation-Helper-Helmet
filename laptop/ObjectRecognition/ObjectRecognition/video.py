#-------------------------------------#
#       调用摄像头检测
#-------------------------------------#
from keras.layers import Input
from yolo import YOLO
from PIL import Image
import numpy as np
import cv2
import time
import zmq
import base64

yolo = YOLO()
# 调用摄像头
#capture=cv2.VideoCapture(0) # capture=cv2.VideoCapture("1.mp4")
"""实例化用来接收帧的zmq对象"""
context = zmq.Context()
"""zmq对象建立TCP链接"""
footage_socket = context.socket(zmq.PAIR)
footage_socket.bind('tcp://*:5555')
fps = 0.0
while(True):
    frame_camera = footage_socket.recv_string()  # 接收TCP传输过来的一帧视频图像数据
    img = base64.b64decode(frame_camera)  # 把数据进行base64解码后储存到内存img变量中
    npimg = np.frombuffer(img, dtype=np.uint8)  # 把这段缓存解码成一维数组
    source = cv2.imdecode(npimg, 1)  # 将一维数组解码为图像source
    t1 = time.time()
    # 读取某一帧
    frame = source
    # 格式转变，BGRtoRGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 转变成Image
    frame = Image.fromarray(np.uint8(frame))

    # 进行检测
    frame = np.array(yolo.detect_image(frame))
    # RGBtoBGR满足opencv显示格式
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    fps  = ( fps + (1./(time.time()-t1)) ) / 2
    print("fps= %.2f"%(fps))
    frame = cv2.putText(frame, "fps= %.2f"%(fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("video", frame)
    c= cv2.waitKey(1) & 0xff 
    if c==27:
        capture.release()
        break

yolo.close_session()    
