import cv2

def streamWebcam():

    cv2.namedWindow("Webcam preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 1:  # exit on ESC
            break

    vc.release()
    cv2.destroyWindow("Webcam preview")