#-*- coding: utf-8 -*-

import cv2
from face_train_use_keras import Model
import zmq
import base64
import numpy as np
from yolo import YOLO
from PIL import Image
import time

token = 0

fps = 0

def run():
    global token
    context = zmq.Context()
    """The zmq object establishes a TCP link """
    footage_socket = context.socket(zmq.PAIR)
    footage_socket.bind('tcp://*:5555')
    yolo = YOLO()
    fps = 0.0

    # Load the model
    model = Model()
    model.load_model(file_path='D:/ObjectRecognition/model/me.face.model.h5')

    # The color of the rectangle frame that encloses the face
    color = (0, 255, 0)

    # cap = cv2.VideoCapture(0)

    # Local storage path of face recognition classifier
    cascade_path = "D:/software/Anaconda/pkgs/libopencv-3.4.2-h20b85fd_0/Library/etc/haarcascades/haarcascade_frontalface_alt2.xml"

    out = cv2.VideoWriter()

    sz = (640, 480)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out.open('output.mp4', fourcc, 6, sz, True)
    # Cycle detection and recognition of human faces
    while True:
        frame_camera = footage_socket.recv_string()  # Receive a frame of video image data transmitted by TCP
        img = base64.b64decode(frame_camera)  # The data is base64 decoded and stored in the memory img variable
        npimg = np.frombuffer(img, dtype=np.uint8)  # Decode this buffer into a one-dimensional array
        source = cv2.imdecode(npimg, 1)  # Decode a one-dimensional array into an image source
        # _, frame = cap.read()
        t1 = time.time()
        # Read a frame
        frame = source
        # Format change(BGRtoRGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Turn into Image
        frame = Image.fromarray(np.uint8(frame))

        # Test
        frame = np.array(yolo.detect_image(frame))
        # satisfy the opencv display format
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        fps = (fps + (1. / (time.time() - t1))) / 2
        print("fps= %.2f" % (fps))
        frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # The image is grayed to reduce the computational complexity
        frame_gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)

        # Use face recognition classifier, read into the classifier
        cascade = cv2.CascadeClassifier(cascade_path)

        # Use the classifier to identify which area is a face
        faceRects = cascade.detectMultiScale(frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(faceRects) > 0:
            for faceRect in faceRects:
                x, y, w, h = faceRect

                # Capture the face image and submit it to the model to identify who it is
                image = source[y - 10: y + h + 10, x - 10: x + w + 10]
                faceID = model.face_predict(image)

                if faceID == 0:
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness=2)

                    # text prompt who is the target
                    cv2.putText(frame, 'Junlin Hai',
                                (x + 30, y + 30),  # coordinate
                                cv2.FONT_HERSHEY_SIMPLEX,  # font
                                1,  # size
                                (255, 0, 255),  # color
                                2)  # Word line width

                    file = open('D:/ObjectRecognition/translate/Face_recognition_result.txt', 'w')
                    file.write('Junlin_Hai')
                    # file.close()

                if faceID == 1:
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness=2)

                    cv2.putText(frame, 'Jingwei Yang',
                                (x + 30, y + 30),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (255, 0, 255),
                                2)
                    file = open('D:/ObjectRecognition/translate/Face_recognition_result.txt', 'w')
                    file.write('Jingwei_Yang')
                    # file.close()

                if faceID == 2:
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness=2)


                    cv2.putText(frame, 'Bo Sun',
                                (x + 30, y + 30),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (255, 0, 255),
                                2)
                    file = open('D:/ObjectRecognition/translate/Face_recognition_result.txt', 'w')
                    file.write('Bo_Sun')
                    # file.close()

                if faceID == 3:
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness=2)

                    cv2.putText(frame, 'unknown',
                                (x + 30, y + 30),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (255, 0, 255),
                                2)
                    file = open('D:/ObjectRecognition/translate/Face_recognition_result.txt', 'w')
                    file.write('Unknown')
        file = open('D:/ObjectRecognition/translate/Face_recognition_result.txt', 'w')
        file.write('')

        # Record
        if token == 1:
            cv2.putText(frame, "REC", (550, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            out.write(frame)
            if cv2.waitKey(100) & 0xff == ord('p'):
                # global number
                token = 0
                cv2.putText(frame, " ", (550, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                out.release()
        k = cv2.waitKey(10)

        cv2.imshow("Recognition monitor", frame)

        if k & 0xFF == ord('o'):
            token = 1
        # If you enter q, exit

        if k & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    yolo.close_session()

if __name__ == '__main__':
    run()