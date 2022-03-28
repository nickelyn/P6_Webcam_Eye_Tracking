import cv2

# distance from camera to object(face) measured
# centimeter

Known_distance = 35

# width of face in the real world or Object Plane
# centimeter
Known_width = 16

# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class DistanceDetector:
    def __init__(self):
        self.distance = 0
        self.focal_length_found = 0
        self.ref_image_face_width = 0
        self.face_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.fonts = cv2.FONT_HERSHEY_COMPLEX

    def get_ref_image_face_width(self, ref_image_path):
        ref_image = cv2.imread(ref_image_path)
        self.ref_image_face_width = face_data(ref_image, self.face_detector)

    def find_focal_length(self, ref_distance: int):
        self.focal_length_found = Focal_Length_Finder(
            Known_distance, Known_width, ref_distance
        )

    def get_distance_actual(self, frame):
        face_width_in_frame = face_data(frame, self.face_detector)
        if face_width_in_frame != 0:
            self.distance = Distance_finder(
                self.focal_length_found, Known_width, face_width_in_frame
            )
        else:
            self.distance = 0


def face_data(image, face_detector):
    face_width = 0  # making face width to zero
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detecting face in the image
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    # looping through the faces detect in the image
    # getting coordinates x, y , width and height
    for (x, y, h, w) in faces:
        # draw the rectangle on the face
        cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 2)

        # getting face width in the pixels
        face_width = w

    # return the face width in pixel
    return face_width


def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):
    # finding the focal length
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length


# distance estimation function
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
    distance = (real_face_width * Focal_Length) / face_width_in_frame

    # return the distance
    return distance
