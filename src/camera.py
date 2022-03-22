import numpy as np
import cv2


class Camera:
    def __init__(self, device):
        self.device = device
        self.capture = cv2.VideoCapture(device, cv2.CAP_DSHOW)

        self.is_recording = False

        if not self.capture.isOpened():
            print("Could not access camera!")
            exit()

    def setsize(self, width, height):
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
