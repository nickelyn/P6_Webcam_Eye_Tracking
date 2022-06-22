import numpy as np
import cv2


class Pupil(object):
    """
    Detects the iris of an eye and estimates the position of the pupil.
    """

    def __init__(self, eye_frame):
        self.iris_frame = None
        self.x = None
        self.y = None
        self.detect_iris(eye_frame)

    @staticmethod
    def image_processing(eye_frame):
        """
        Performs operations on the eye frame to isolate the iris.

        Args:
            eye_frame (numpy.ndarray): Frame containing an eye and nothing else.
            threshold (int): Threshold value used to binarize the eye frame.

        Returns:
            A frame with a single element representing the iris.
        """
        new_frame = cv2.adaptiveThreshold(
            eye_frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 3
        )
        new_frame = cv2.bilateralFilter(new_frame, 15, 75, 75)

        return new_frame

    def detect_iris(self, eye_frame):
        """
        Detects the iris and estimates the position of the iris by calculating the centroid.

        Args:
            eye_frame (numpy.ndarray): Frame containing an eye and nothing else.
        """
        self.iris_frame = self.image_processing(eye_frame)

        contours, _ = cv2.findContours(
            self.iris_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
        )[-2:]
        contours = sorted(contours, key=cv2.contourArea)

        try:
            cMax = max(contours, key=cv2.contourArea)
            for (i, ci) in enumerate(contours):
                if len(contours) > 1:
                    removeMax = [c for c in conts2 if c not in cMax]
                    irisContour = max(removeMax, key=cv2.contourArea)
                    moments = cv2.moments(irisContour)
                    self.x = int(moments["m10"] / moments["m00"])
                    self.y = int(moments["m01"] / moments["m00"])
                    # TODO: Lav en toggle funktion sådan at man kan slå cirklen om iris fra / til
                    # cv2.circle(image, (cx, cy), 5, (0, 225, 0), 1)

        except (IndexError, ZeroDivisionError):
            pass
