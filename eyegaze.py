import cv2
import numpy as np
import dlib
from math import hypot


def findMidPoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


def getFace():
    # Use the d.lib frontal face detector
    detector = dlib.get_frontal_face_detector()

    # Use the d.lib to predict facial landmarks / shapes
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # Obtain feed from webcam
    camFeed = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        _, frame = camFeed.read()
        # Turn the feed into grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Get an array of faces from webcam feed
        faces = detector(gray)

        # Loop through the array
        for face in faces:
            # Finds the upper left and top coordinate
            # Values start from 0 and the further away one is, from i.e. left part of screen, the higher the value gets
            # xleft, ytop = face.left(), face.top()
            # End the lower left and bottom coordinate
            # xright, ybottom = face.right(), face.bottom()
            # Create a green frame around the face
            # cv2.rectangle(gray, (face.left(), face.top()), (xright, ybottom), (0, 255, 0), 2)

            # Create a predictor for landmarks to be found in the face
            landmarks = predictor(gray, face)
            # Find the leftmost point of the left eye
            le_left_point = (landmarks.part(36).x, landmarks.part(36).y)
            # Find the rightmost point of the left eye
            le_right_point = (landmarks.part(39).x, landmarks.part(39).y)

            # Finds the middle point between the horizontal line in the eye
            le_center_top_point = findMidPoint(
                landmarks.part(37), landmarks.part(38)
            )
            le_center_bottom_point = findMidPoint(
                landmarks.part(41), landmarks.part(40)
            )

            # Find the leftmost point of the right eye
            re_left_point = (landmarks.part(42).x, landmarks.part(42).y)

            # Find the rightmost point of the right eye
            re_right_point = (landmarks.part(45).x, landmarks.part(45).y)

            # Finds the middle point between the horizontal line in the eye
            re_center_top_point = findMidPoint(
                landmarks.part(43), landmarks.part(44)
            )
            re_center_bottom_point = findMidPoint(
                landmarks.part(47), landmarks.part(46)
            )

            # Create the horizontal and vertical line (left eye)
            le_horizontal_line = cv2.line(
                frame, le_left_point, le_right_point, (0, 255, 0), 1
            )
            le_vertical_line = cv2.line(
                frame,
                le_center_top_point,
                le_center_bottom_point,
                (0, 255, 0),
                1,
            )

            # Create the horizontal and vertical line (right eye)
            re_horizontal_line = cv2.line(
                frame, re_left_point, re_right_point, (0, 255, 0), 1
            )
            re_vertical_line = cv2.line(
                frame,
                re_center_top_point,
                re_center_bottom_point,
                (0, 255, 0),
                1,
            )

            # Find the length of the vertical line for the right and left eye
            re_vertical_line_len = hypot(
                (re_center_top_point[0] - re_center_bottom_point[0]),
                (re_center_top_point[1] - re_center_bottom_point[1]),
            )

            le_vertical_line_len = hypot(
                (le_center_top_point[0] - le_center_bottom_point[0]),
                (le_center_top_point[1] - le_center_bottom_point[1]),
            )

            # Find the length of the horizontal line for right and left eye
            re_horizontal_line_len = hypot(
                (re_left_point[0] - re_right_point[0]),
                (re_left_point[1] - re_right_point[1]),
            )

            le_horizontal_line_len = hypot(
                (le_left_point[0] - le_right_point[0]),
                (le_left_point[1] - le_right_point[1]),
            )

            # Calculate the ratio between eye height and width
            ratio_LE = le_horizontal_line_len / le_vertical_line_len
            ratio_RE = re_horizontal_line_len / re_vertical_line_len

            # print("RE: " + str(ratio_RE))
            # print("LE: " + str(ratio_LE))

            # Needs optimization, only works at a specific distance and that very well
            if ratio_LE > 4.7 and ratio_RE > 4.7:
                cv2.putText(
                    frame, "BOTH EYES CLOSED", (50, 150), font, 1, (0, 0, 255)
                )
            elif ratio_LE > 4.7:
                cv2.putText(
                    frame, "RIGHT EYE CLOSED", (50, 150), font, 1, (0, 0, 255)
                )
            elif ratio_RE > 4.7:
                cv2.putText(
                    frame, "LEFT EYE CLOSED", (50, 150), font, 1, (0, 0, 255)
                )

            # Eye Gaze
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

            # cv2.polylines(frame, [left_eye_outline], True, (0, 255, 0), 1)

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

            # cv2.polylines(frame, [right_eye_outline], True, (0, 255, 0), 1)

            # Get the height and width of the frame object
            height, width, _ = frame.shape

            # Create a mask of the entire face but the eyes
            mask = np.zeros((height, width), np.uint8)
            cv2.polylines(mask, [left_eye_outline], True, 255, 2)
            cv2.fillPoly(mask, [left_eye_outline], 255)
            left_eye = cv2.bitwise_and(gray, gray, mask=mask)

            # Find min / max points of eye shape
            min_x = np.min(left_eye_outline[:, 0])
            max_x = np.max(left_eye_outline[:, 0])
            min_y = np.min(left_eye_outline[:, 1])
            max_y = np.max(left_eye_outline[:, 1])

            gray_eye = left_eye[min_y:max_y, min_x:max_x]
            _, threshold_eye = cv2.threshold(
                gray_eye, 70, 255, cv2.THRESH_BINARY
            )

            eye = cv2.resize(gray_eye, None, fx=5, fy=5)
            threshold_eye = cv2.resize(threshold_eye, None, fx=5, fy=5)

            cv2.imshow("Black eye", threshold_eye)
            cv2.imshow("Eye", eye)
            cv2.imshow("Threshold", threshold_eye)
            cv2.imshow("Left eye", mask)
        cv2.imshow("Webcam feed", frame)
        # Option - press esc to quit the feed
        key = cv2.waitKey(1)
        if key == 27:
            break

    camFeed.release()
    cv2.destroyAllWindows()
