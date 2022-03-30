import cv2
import dlib
from math import hypot


class Gaze:
    def __init__(self):
        self.landmarks = None
        self.faces = None
        self.grey = None
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def feed_frame(self, frame):
        self.grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def find_faces(self):
        self.faces = self.detector(self.grey)

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


def handle_faces(gaze: Gaze, frame, lle=False, lre=False):
    for face in gaze.faces:
        gaze.find_landmarks(face)
        points = find_points_in_eye(gaze.landmarks)
        if lle:
            lines_in_left_eye(frame, points)
        if lre:
            lines_in_right_eye(frame, points)


def lines_in_left_eye(frame, points):
    # Create the horizontal and vertical line (left eye)
    le_horizontal_line = cv2.line(frame, points[0], points[1], (0, 255, 0), 1)
    le_vertical_line = cv2.line(
        frame,
        points[2],
        points[3],
        (0, 255, 0),
        1,
    )


def lines_in_right_eye(frame, points):
    # Create the horizontal and vertical line (left eye)
    re_horizontal_line = cv2.line(frame, points[4], points[5], (0, 255, 0), 1)
    re_vertical_line = cv2.line(frame, points[6], points[7], (0, 255, 0), 1)


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
