import numpy as np
import cv2


class Camera:
    def __init__(self, device):
        self.device = device
        self.capture = cv2.VideoCapture(device)

        self.is_recording = False

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

        if not self.capture.isOpened():
            print("Could not access camera!")
            exit()
