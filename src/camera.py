import sys

import cv2 as cv
import platform as p


class Camera:
    def __init__(self, device: int):
        self.device = device
        if get_OS() == "Darwin":
            self.capture = cv.VideoCapture(device, cv.CAP_AVFOUNDATION)
        else:
            self.capture = cv.VideoCapture(device, cv.CAP_DSHOW)

        self.is_showing = False

        if not self.capture.isOpened():
            sys.exit()

    def setsize(self, width: int, height: int):
        self.capture.set(cv.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv.CAP_PROP_FRAME_HEIGHT, height)


def get_OS():
    if p.system() == "Darwin":
        os = "Darwin"
    elif p.system() == "Windows":
        os = "Windows"
    elif p.system() == "Linux":
        os = "Linux"
    else:
        os = "Unknown"
    return os
