import os
import sys
import cv2 as cv
import dlib

from .eye import Eye
from .calibration import Calibration

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)

from definitions import *


class GazeTracking(object):
    def __init__(self):
        self.frame = None
        self.eye_left = None
        self.eye_right = None
        self.calibration = Calibration()

        # _face_detector is used to detect faces
        self._face_detector = dlib.get_frontal_face_detector()

        # _predictor is used to get facial landmarks of a given face
        model_path = os.path.join(
            DATA_DIR, "models/shape_predictor_68_face_landmarks.dat"
        )
        self._predictor = dlib.shape_predictor(model_path)

    @property
    def pupils_located(self):
        try:
            int(self.eye_left.pupil.x)
            int(self.eye_left.pupil.y)
            int(self.eye_right.pupil.x)
            int(self.eye_right.pupil.y)
            return True
        except Exception:
            return False

    def _analyze(self):
        """Detects the face and initialize Eye objects"""
        frame = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        faces = self._face_detector(frame)

        try:
            landmarks = self._predictor(frame, faces[0])
            self.eye_left = Eye(frame, landmarks, 0, self.calibration)
            self.eye_right = Eye(frame, landmarks, 1, self.calibration)



        except IndexError:
            self.eye_left = None
            self.eye_right = None

    def refresh(self, frame):
        """Refreshes the frame and analyzes it.

        Arguments:
            frame (numpy.ndarray): The frame to analyze
        """
        self.frame = frame
        self._analyze()

    def get_pupil_coords_left(self):
        """Returns the coordinates of the left pupil"""
        if self.pupils_located:
            x = self.eye_left.pupil.x
            y = self.eye_left.pupil.y
            return (x, y)

    def get_pupil_coords_right(self):
        """Returns the coordinates of the right pupil"""
        if self.pupils_located:
            x = self.eye_right.pupil.x
            y = self.eye_right.pupil.y
            return (x, y)

    def hori_ratio(self):
        """Returns a number between 0.0 and 1.0 that indicates the
        horizontal direction of the gaze. The extreme right is 0.0,
        the center is 0.5 and the extreme left is 1.0
        """
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.x / (self.eye_left.center[0] * 2 - 10)
            pupil_right = self.eye_right.pupil.x / (self.eye_right.center[0] * 2 - 10)
            return (pupil_left + pupil_right) / 2
        else:
            return -1

    def vert_ratio(self):
        """Returns a number between 0.0 and 1.0 that indicates the
        vertical direction of the gaze. The extreme top is 0.0,
        the center is 0.5 and the extreme bottom is 1.0
        """
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.y / (self.eye_left.center[1] * 2 - 10)
            pupil_right = self.eye_right.pupil.y / (self.eye_right.center[1] * 2 - 10)
            return (pupil_left + pupil_right) / 2

    def is_right(self):
        """Returns true if the user is looking to the right"""
        if self.pupils_located:
            return self.hori_ratio() <= 0.65

    def is_left(self):
        """Returns true if the user is looking to the left"""
        if self.pupils_located:
            return self.hori_ratio() >= 0.85

    def is_up(self):
        if self.pupils_located:
            return self.vert_ratio() <= 1.2

    def is_down(self):
        if self.pupils_located:
            return self.vert_ratio() >= 1.3

    def is_center(self):
        """Returns true if the user is looking to the center"""
        if self.pupils_located:
            return (
                self.is_right() is not True
                and self.is_left() is not True
                and self.is_up() is not True
                and self.is_down() is not True
            )

    def is_blinking(self):
        """Returns true if the user closes his eyes"""
        if self.pupils_located:
            blinking_ratio = (self.eye_left.blinking + self.eye_right.blinking) / 2
            return blinking_ratio > 3.8

    def annotated_frame(self):
        """Returns the main frame with pupils highlighted"""
        frame = self.frame.copy()

        if self.pupils_located:
            color = (0, 255, 0)
            x_left, y_left = self.get_pupil_coords_left()
            x_right, y_right = self.get_pupil_coords_right()
            cv.line(frame, (x_left - 5, y_left), (x_left + 5, y_left), color)
            cv.line(frame, (x_left, y_left - 5), (x_left, y_left + 5), color)
            cv.line(frame, (x_right - 5, y_right), (x_right + 5, y_right), color)
            cv.line(frame, (x_right, y_right - 5), (x_right, y_right + 5), color)

        return frame
