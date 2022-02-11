import numpy as np
import cv2

cap = cv2.VideoCapture(0)

## some videowriter props
sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
      int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

fps = 20
# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# fourcc = cv2.VideoWriter_fourcc('m', 'p', 'e', 'g')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

## open and set props
out = cv2.VideoWriter()
out.open('output.mp4', fourcc, fps, sz, True)

while (True):
    ret, frame = cap.read()
    out.write(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()