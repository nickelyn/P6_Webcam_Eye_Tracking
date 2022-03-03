import numpy as np
import cv2 as cv
import argparse

parser = argparse.ArgumentParser(description='webcam eye tracking.')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('haarcascade_righteye_2splits.xml')

camera_device = args.camera
capture = cv.VideoCapture(camera_device)

if not capture.isOpened():
    print("Cannot open camera!")
    exit()
while capture.isOpened():
    # frame by frame
    ret, frame = capture.read()

        # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
capture.release()
cv.destroyAllWindows()
