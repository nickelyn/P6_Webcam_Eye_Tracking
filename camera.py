import numpy as np
import cv2


class Camera:
    def __init__(self, device):
        self.device = device
        self.capture = cv2.VideoCapture(device)

        self.is_recording = False

        if not self.capture.isOpened():
            print("Could not access camera!")
            exit()
