import cv2
import platform as p


class Camera:
    def __init__(self, device):
        self.device = device
        if determine_mac_os():
            self.capture = cv2.VideoCapture(device, cv2.CAP_AVFOUNDATION)
        else:
            self.capture = cv2.VideoCapture(device, cv2.CAP_DSHOW)

        self.is_recording = False

        if not self.capture.isOpened():
            print("Could not access camera!")
            exit()

    def setsize(self, width, height):
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def determine_mac_os():
    if p.system() == "Darwin":
        return True
    return False
