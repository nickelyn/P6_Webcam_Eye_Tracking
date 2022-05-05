import os
import sys
import cv2 as cv
import dlib
from math import hypot
from distance_detection.distance_detector import DistanceDetector
import distance_detection.distance_detector as dt

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)

from definitions import *

import numpy as np

font = cv.FONT_HERSHEY_SIMPLEX


class Gaze:
    def __init__(self):
        self.ref_image_width = 0
        self.landmarks = None
        self.faces = None
        self.grey = None
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(
            os.path.join(DATA_DIR, "models/shape_predictor_68_face_landmarks.dat")
        )
        self.distance_detector = DistanceDetector()
        self.ref_image = cv.imread(os.path.join(DATA_DIR, "images/ref_image_new.jpg"))

    def feed_frame(self, frame):
        try:
            self.grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            return True
        except:
            return False

    def find_faces(self):
        self.faces = self.detector(self.grey)

    def find_ref_image_width(self):
        self.ref_image_width = dt.face_data(
            self.ref_image, self.distance_detector.face_detector
        )
        self.distance_detector.find_focal_length(self.ref_image_width)

    def find_landmarks(self, face):
        self.landmarks = self.predictor(self.grey, face)


def prepare_gaze_object(gaze: Gaze, frame):
    gaze.feed_frame(frame)
    gaze.find_faces()
    return gaze


def findMidPoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


def getRatio(horizontal, vertical):
    return horizontal / vertical


def getVerticalLen(
    centertoppoint1, centertoppoint2, centerbottompoint1, centerbottompoint2
):
    vertical_line_len = hypot(
        (centertoppoint1 - centerbottompoint1), (centertoppoint2 - centerbottompoint2)
    )
    return vertical_line_len


def handle_faces(
    gaze: Gaze,
    frame,
    lle=False,
    lre=False,
    closed=False,
    outline=False,
    ratio=False,
    distance=False,
):
    outlines = list()
    for face in gaze.faces:
        gaze.find_landmarks(face)
        points = find_points_in_eye(gaze.landmarks)
        if lle:
            lines_in_left_eye(frame, points)
        if lre:
            lines_in_right_eye(frame, points)
        if closed:
            find_vertical_and_horizontal_length_ratio(points, frame)
        if outline or ratio:
            outlines = outline_eyes(gaze.landmarks, frame, outline=outline)
        if ratio:
            calculate_ratio(frame=frame, outlines=outlines, gaze=gaze)
        if distance:
            handle_distance(gaze=gaze, frame=frame)


def lines_in_left_eye(frame, points):
    # Create the horizontal and vertical line (left eye)
    le_horizontal_line = cv.line(frame, points[0], points[1], (0, 255, 0), 1)
    le_vertical_line = cv.line(
        frame,
        points[2],
        points[3],
        (0, 255, 0),
        1,
    )


def lines_in_right_eye(frame, points):
    # Create the horizontal and vertical line (left eye)
    re_horizontal_line = cv.line(frame, points[4], points[5], (0, 255, 0), 1)
    re_vertical_line = cv.line(frame, points[6], points[7], (0, 255, 0), 1)


def find_points_in_eye(landmarks):
    le_left_point = (landmarks.part(36).x, landmarks.part(36).y)
    le_right_point = (landmarks.part(39).x, landmarks.part(39).y)

    # Finds the middle point between the horizontal line in the eye
    le_center_top_point = findMidPoint(landmarks.part(37), landmarks.part(38))
    le_center_bottom_point = findMidPoint(landmarks.part(41), landmarks.part(40))

    # Find the left- and rightmost points of the right eye
    re_left_point = (landmarks.part(42).x, landmarks.part(42).y)
    re_right_point = (landmarks.part(45).x, landmarks.part(45).y)

    # Finds the middle point between the horizontal line in the eye
    re_center_top_point = findMidPoint(landmarks.part(43), landmarks.part(44))
    re_center_bottom_point = findMidPoint(landmarks.part(47), landmarks.part(46))

    return [
        le_left_point,
        le_right_point,
        le_center_top_point,
        le_center_bottom_point,
        re_left_point,
        re_right_point,
        re_center_top_point,
        re_center_bottom_point,
    ]


def find_vertical_and_horizontal_length_ratio(points: list, frame):
    re_vertical_line_len = getVerticalLen(
        points[6][0],
        points[6][1],
        points[7][0],
        points[7][1],
    )
    le_vertical_line_len = getVerticalLen(
        points[2][0],
        points[3][0],
        points[2][1],
        points[3][1],
    )
    re_horizontal_line_len = getVerticalLen(
        points[4][0], points[5][0], points[4][1], points[5][1]
    )
    le_horizontal_line_len = getVerticalLen(
        points[0][0], points[1][0], points[0][1], points[1][1]
    )
    ratio_LE = getRatio(le_horizontal_line_len, le_vertical_line_len)
    ratio_RE = getRatio(re_horizontal_line_len, re_vertical_line_len)

    if ratio_LE > 4.7 and ratio_RE > 4.7:
        cv.putText(frame, "BOTH EYES CLOSED", (50, 150), font, 1, (0, 0, 255))
    elif ratio_LE > 4.7:
        cv.putText(frame, "RIGHT EYE CLOSED", (50, 150), font, 1, (0, 0, 255))
    elif ratio_RE > 4.7:
        cv.putText(frame, "LEFT EYE CLOSED", (50, 150), font, 1, (0, 0, 255))

    # return [ratio_LE, ratio_RE]


def outline_eyes(landmarks, frame, outline=False):
    left_eye_outline = np.array(
        [
            (landmarks.part(36).x, landmarks.part(36).y),
            (landmarks.part(37).x, landmarks.part(37).y),
            (landmarks.part(38).x, landmarks.part(38).y),
            (landmarks.part(39).x, landmarks.part(39).y),
            (landmarks.part(40).x, landmarks.part(40).y),
            (landmarks.part(41).x, landmarks.part(41).y),
        ],
        np.int32,
    )

    right_eye_outline = np.array(
        [
            (landmarks.part(42).x, landmarks.part(42).y),
            (landmarks.part(43).x, landmarks.part(43).y),
            (landmarks.part(44).x, landmarks.part(44).y),
            (landmarks.part(45).x, landmarks.part(45).y),
            (landmarks.part(46).x, landmarks.part(46).y),
            (landmarks.part(47).x, landmarks.part(47).y),
        ],
        np.int32,
    )

    if outline:
        cv.polylines(frame, [right_eye_outline], True, (0, 255, 0), 1)
        cv.polylines(frame, [left_eye_outline], True, (0, 255, 0), 1)

    return [left_eye_outline, right_eye_outline]


def calculate_ratio(frame, outlines: list, gaze: Gaze):
    # Get the height and width of the frame object
    height, width, _ = frame.shape

    left_eye = createMask(height, width, gaze.grey, outlines[0])
    right_eye = createMask(height, width, gaze.grey, outlines[1])

    # Find min / max points of eye shape
    min_x = np.min(outlines[0][:, 0])
    max_x = np.max(outlines[0][:, 0])
    min_y = np.min(outlines[0][:, 1])
    max_y = np.max(outlines[0][:, 1])

    gray_eye = left_eye[min_y:max_y, min_x:max_x]
    _, threshold_eye = cv.threshold(gray_eye, 70, 255, cv.THRESH_BINARY)

    heightShape, widthShape = threshold_eye.shape

    # Split the eye in 2 sides (left and right)
    left_side_threshold = threshold_eye[0:heightShape, 0 : int(widthShape / 2)]
    left_side_white = cv.countNonZero(left_side_threshold)
    right_side_threshold = threshold_eye[0:height, int(widthShape / 2) : widthShape]
    right_side_white = cv.countNonZero(right_side_threshold)

    # Calculate the gaze ratio
    gaze_ratio = (left_side_white + np.finfo(float).eps) / (
        right_side_white + np.finfo(float).eps
    )
    # Put ratio in the webcam feed
    cv.putText(frame, str(gaze_ratio), (50, 100), font, 2, (0, 255, 0), 3)
    # Resize the scale
    threshold_eye = cv.resize(threshold_eye, None, fx=5, fy=5)
    eye = cv.resize(gray_eye, None, fx=5, fy=5)


def createMask(height, width, gray, eye_outline):
    # Create a mask of the entire face but the eyes
    mask = np.zeros((height, width), np.uint8)
    cv.polylines(mask, [eye_outline], True, 255, 2)
    cv.fillPoly(mask, [eye_outline], 255)
    left_eye = cv.bitwise_and(gray, gray, mask=mask)
    return left_eye


def handle_distance(gaze: Gaze, frame):
    gaze.distance_detector.get_distance_actual(frame)
    cv.putText(
        frame,
        str(f"Distance = {gaze.distance_detector.distance}"),
        (50, 100),
        font,
        2,
        (0, 255, 0),
        3,
    )
