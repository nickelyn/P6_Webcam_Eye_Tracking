import cv2
import numpy as np
import dlib
from math import hypot


def findMidPoint(p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def setDetector():
    # Use the d.lib frontal face detector
    detector = dlib.get_frontal_face_detector()
    return detector

def setPredictor():
    #Use the d.lib to predict facial landmarks / shapes
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    return predictor

def getFeed():
    #Obtain feed from webcam
    camFeed = cv2.VideoCapture(0)
    return camFeed

def getRatio(horizontal, vertical):
    return horizontal / vertical

def getVerticalLen(centertoppoint1, centertoppoint2, centerbottompoint1, centerbottompoint2):
    vertical_line_len = hypot((centertoppoint1 - centerbottompoint1),
                                 (centertoppoint2 - centerbottompoint2))
    return vertical_line_len


def createMask(height, width, gray, eye_outline):
    #Create a mask of the entire face but the eyes
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [eye_outline], True, 255, 2)
    cv2.fillPoly(mask, [eye_outline], 255)
    left_eye = cv2.bitwise_and(gray, gray, mask=mask)
    return left_eye

def getFace():

    detector = setDetector()

    # Use the d.lib to predict facial landmarks / shapes
    predictor = setPredictor()
    camFeed = getFeed()
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        _, frame = camFeed.read()
        # Turn the feed into grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Get an array of faces from webcam feed
        faces = detector(gray)

        # Loop through the array of faces from detector
        for face in faces:

            # Create a predictor for landmarks to be found in the face
            landmarks = predictor(gray, face)

            #Find the left- and rightmost points of the left eye
            le_left_point = (landmarks.part(36).x, landmarks.part(36).y)
            le_right_point = (landmarks.part(39).x, landmarks.part(39).y)

            #Finds the middle point between the horizontal line in the eye
            le_center_top_point = findMidPoint(landmarks.part(37), landmarks.part(38))
            le_center_bottom_point = findMidPoint(landmarks.part(41), landmarks.part(40))

            #Find the left- and rightmost points of the right eye
            re_left_point = (landmarks.part(42).x, landmarks.part(42).y)
            re_right_point = (landmarks.part(45).x, landmarks.part(45).y)

            # Finds the middle point between the horizontal line in the eye
            re_center_top_point = findMidPoint(landmarks.part(43), landmarks.part(44))
            re_center_bottom_point = findMidPoint(landmarks.part(47), landmarks.part(46))

            # Create the horizontal and vertical line (left eye)
            le_horizontal_line = cv2.line(frame, le_left_point, le_right_point, (0, 255, 0), 1)
            le_vertical_line = cv2.line(frame, le_center_top_point, le_center_bottom_point, (0, 255, 0), 1)

            # Create the horizontal and vertical line (right eye)
            re_horizontal_line = cv2.line(frame, re_left_point, re_right_point, (0, 255, 0), 1)
            re_vertical_line = cv2.line(frame, re_center_top_point, re_center_bottom_point, (0, 255, 0), 1)

            #Find the length of the vertical line for the right and left eye
            re_vertical_line_len = getVerticalLen(re_center_top_point[0], re_center_top_point[1], re_center_bottom_point[0], re_center_bottom_point[1])

            le_vertical_line_len = getVerticalLen(le_center_top_point[0], le_center_bottom_point[0], le_center_top_point[1], le_center_bottom_point[1])

            #Find the length of the horizontal line for right and left eye
            re_horizontal_line_len = getVerticalLen(re_left_point[0], re_right_point[0], re_left_point[1], re_right_point[1])

            le_horizontal_line_len = getVerticalLen(le_left_point[0], le_right_point[0], le_left_point[1], le_right_point[1])

            #Calculate the ratio between eye height and width
            ratio_LE = getRatio(le_horizontal_line_len, le_vertical_line_len)
            ratio_RE = getRatio(re_horizontal_line_len, re_vertical_line_len)

            if ratio_LE > 4.7 and ratio_RE > 4.7:
                cv2.putText(frame, "BOTH EYES CLOSED", (50, 150), font, 1, (0, 0, 255))
            elif ratio_LE > 4.7:
                cv2.putText(frame, "RIGHT EYE CLOSED", (50, 150), font, 1, (0, 0, 255))
            elif ratio_RE > 4.7:
                cv2.putText(frame, "LEFT EYE CLOSED", (50, 150), font, 1, (0, 0, 255))

            # Eye Gaze
            left_eye_outline = np.array([(landmarks.part(36).x, landmarks.part(36).y),
                                         (landmarks.part(37).x, landmarks.part(37).y),
                                         (landmarks.part(38).x, landmarks.part(38).y),
                                         (landmarks.part(39).x, landmarks.part(39).y),
                                         (landmarks.part(40).x, landmarks.part(40).y),
                                         (landmarks.part(41).x, landmarks.part(41).y)], np.int32)

            # cv2.polylines(frame, [left_eye_outline], True, (0, 255, 0), 1)

            right_eye_outline = np.array([(landmarks.part(42).x, landmarks.part(42).y),
                                          (landmarks.part(43).x, landmarks.part(43).y),
                                          (landmarks.part(44).x, landmarks.part(44).y),
                                          (landmarks.part(45).x, landmarks.part(45).y),
                                          (landmarks.part(46).x, landmarks.part(46).y),
                                          (landmarks.part(47).x, landmarks.part(47).y)], np.int32)

            # cv2.polylines(frame, [right_eye_outline], True, (0, 255, 0), 1)

            #Get the height and width of the frame object
            height, width, _ = frame.shape

            left_eye = createMask(height, width, gray, left_eye_outline)
            right_eye = createMask(height, width, gray, right_eye_outline)

            #Find min / max points of eye shape
            min_x = np.min(left_eye_outline[:, 0])
            max_x = np.max(left_eye_outline[:, 0])
            min_y = np.min(left_eye_outline[:, 1])
            max_y = np.max(left_eye_outline[:, 1])

            gray_eye = left_eye[min_y: max_y, min_x: max_x]
            _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)

            cv2.imshow("Threshold", threshold_eye)
            heightShape, widthShape = threshold_eye.shape

            #Split the eye in 2 sides (left and right)
            left_side_threshold = threshold_eye[0: heightShape, 0: int(widthShape/2)]
            left_side_white = cv2.countNonZero(left_side_threshold)
            right_side_threshold = threshold_eye[0: height, int(widthShape/2): widthShape]
            right_side_white = cv2.countNonZero(right_side_threshold)

            #Calculate the gaze ratio
            gaze_ratio = (left_side_white + np.finfo(float).eps)/(right_side_white + np.finfo(float).eps)
            #Put ratio in the webcam feed
            cv2.putText(frame, str(gaze_ratio), (50, 100), font, 2, (0, 255, 0), 3)
            #Resize the scale
            threshold_eye = cv2.resize(threshold_eye, None, fx=5, fy=5)
            eye = cv2.resize(gray_eye, None, fx=5, fy=5)

            #cv2.imshow("Left", left_side_threshold)
            #cv2.imshow("Right", right_side_threshold)

            #Show the webcam feed
            cv2.imshow("Webcam feed", frame)
        #Option - press esc to quit the feed
        key = cv2.waitKey(1)
        if key == 27:
            break

    camFeed.release()
    cv2.destroyAllWindows()