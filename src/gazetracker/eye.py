import math

import cv2 as cv
import numpy as np
from .pupil import Pupil


class Eye(object):
    LEFT_EYE_POINTS = [36, 37, 38, 39, 40, 41]
    RIGHT_EYE_POINTS = [42, 43, 44, 45, 46, 47]

    def __init__(self, original_frame, landmarks, side, calibration):
        self.frame = None
        self.pupil = None
        self.landmark_points = None

        self.analyse(original_frame, landmarks, side, calibration)

    @staticmethod
    def middle_point(p1, p2):
        """
        Computes the middle point between two points.

        Args:
            p1 (dlib.point): First point.
            p2 (dlib.point): Second point.

        Returns:
            The middle point (x,y) between two points.
        """
        x = int((p1.x + p2.x) / 2)
        y = int((p1.y + p2.y) / 2)
        return x, y

    def isolate(self, frame, landmarks, points):
        """
        Isolates an eye to have a frame without other parts of a face.

        Args:
            frame (numpy.ndarray): Frame containing the face.
            landmarks (dlib.full_object_detection): Facial landmarks for the face region.
            points (list): Points of an eye (from the 68 Multi-PIE landmarks).
        """
        coords = np.zeros((68, 2), dtype="int")
        for i in range(0, 68):
            coords[i] = (cord.part(i).x, cord.part(i).y)

        points = [coords[i] for i in side]
        points = np.array(points, dtype=np.int32)
        self.landmark_points = points

        # Apply mask to exclude everything but the eye
        black_frame = np.zeros(frame.shape[:2], np.uint8)
        conts, _ = cv2.findContours(points, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        x, y, w, h = cv2.boundingRect(conts[0])

        min_x = x - 5
        max_x = x + w
        min_y = y - 6
        max_y = y + h + 3

        points = np.array(
            [
                [(x - 5), (y - 6)],
                [(x + w), (y - 6)],
                [(x + w), (y + 3 + h)],
                [(x - 5), (y + 3 + h)],
            ],
            dtype=np.int32,
        )
        mask = cv2.fillConvexPoly(mask, points, 255)
        cv2.dilate(mask, None, iterations=9)
        eye = cv2.bitwise_and(black_frame, frame.copy(), mask=mask)

        # Cropping the eye
        self.frame = eye[min_y:max_y, min_x:max_x]

        height, width = self.frame.shape[:2]

    def blinking_ratio(self, landmarks, points):
        """
        Calculates a ratio that can indicate whether an eye is closed or not.
        It is the division of the width of the eye by its height.

        Args:
            landmarks (dlib.full_object_detection): Facial landmarks for the face region.
            points (list): Points of an eye (from the 68 Multi-PIE landmarks).

        Returns:
            A computed ratio.
        """
        left = (landmarks.part(points[0]).x, landmarks.part(points[0]).y)
        right = (landmarks.part(points[3]).x, landmarks.part(points[3]).y)
        top = self.middle_point(landmarks.part(points[1]), landmarks.part(points[2]))
        bottom = self.middle_point(landmarks.part(points[5]), landmarks.part(points[4]))

        eye_width = math.hypot((left[0] - right[0]), (left[1] - right[1]))
        eye_height = math.hypot((top[0] - bottom[0]), (top[1] - bottom[1]))

        try:
            ratio = eye_width / eye_height
        except ZeroDivisionError:
            ratio = None

        return ratio

    def analyse(self, original_frame, landmarks, side, calibration):
        """
        Detects and isolates the eye in a new frame. Sends the data to the calibration,
        and initialises Pupil object.

        Args:
            original_frame (numpy.ndarray): Frame passed by the user.
            landmarks (dlib.full_object_detection): Facial landmarks for the face region.
            side: Indicates whether it's the left eye (0) or the right eye (1).
            calibration (calibration.Calibration): Manages the binarisation threshold value.
        """
        if side == 0:
            points = self.LEFT_EYE_POINTS
        elif side == 1:
            points = self.RIGHT_EYE_POINTS
        else:
            return

        self.blinking = self.blinking_ratio(landmarks, points)
        self.isolate(original_frame, landmarks, points)

        if not calibration.is_complete():
            calibration.evaluate(self.frame, side)

        threshold = calibration.threshold(side)
        self.pupil = Pupil(self.frame, threshold)
