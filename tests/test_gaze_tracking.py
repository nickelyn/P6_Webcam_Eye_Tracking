import os
import unittest

from PIL import Image
import numpy as np

from src.gazetracker.gaze_tracking import GazeTracking
import definitions as defs


class TestGazeTracking(unittest.TestCase):
    def setUp(self):
        self.gazetracker = GazeTracking()
        ref_image_path = os.path.join(defs.DATA_DIR, "images/ref_image_new.jpg")
        image = Image.open(ref_image_path)
        self.frame = np.array(image)
        image.close()

        ref_image_path = os.path.join(defs.DATA_DIR, "images/ref_image_closed.jpg")
        image = Image.open(ref_image_path)
        self.frame_closed = np.array(image)
        image.close()


    # This test also test the Eye.py by default
    def test_refresh_frame(self):
        self.gazetracker.refresh(self.frame)

        self.assertIsNotNone(self.gazetracker.eye_left)
        self.assertIsNotNone(self.gazetracker.eye_right)

    def test_pupils_located(self):
        # Arrange
        self.gazetracker.refresh(self.frame)
        located = self.gazetracker.pupils_located

        self.gazetracker.refresh(self.frame_closed)
        located_false = self.gazetracker.pupils_located

        # Assert
        self.assertEqual(located, True)
        self.assertEqual(located_false, False)

    def test_get_pupil_coords(self):
        self.gazetracker.refresh(self.frame)

        left = self.gazetracker.get_pupil_coords_left()
        right = self.gazetracker.get_pupil_coords_right()

        self.assertEqual(left, (578, 422))
        self.assertEqual(right, (730, 437))

    def test_blinking(self):
        self.gazetracker.refresh(self.frame)
        self.gazetracker.annotated_frame()
        blinking = self.gazetracker.is_blinking()
        self.gazetracker.refresh(self.frame_closed)
        self.gazetracker.annotated_frame()
        blinking_true = self.gazetracker.is_blinking()

        self.assertEqual(False, blinking)
        self.assertEqual(None, blinking_true)

    def test_ratios(self):
        self.gazetracker.refresh(self.frame)
        self.gazetracker.annotated_frame()

        hor = self.gazetracker.hori_ratio()
        ver = self.gazetracker.vert_ratio()

        self.assertIsNotNone(hor)
        self.assertIsNotNone(ver)

    def test_eye_blinking(self):
        self.gazetracker.refresh(self.frame)

        right_blink = self.gazetracker.eye_right.blinking
        left_blink = self.gazetracker.eye_left.blinking

        self.assertIsNotNone(right_blink)
        self.assertIsNotNone(left_blink)

    def test_pupil_iris_frame(self):
        self.gazetracker.refresh(self.frame)

        iris_frame_left = self.gazetracker.eye_left.pupil.iris_frame
        iris_frame_right = self.gazetracker.eye_right.pupil.iris_frame

        self.assertIsNotNone(iris_frame_left)
        self.assertIsNotNone(iris_frame_right)

    def test_pupil_x_and_y(self):
        self.gazetracker.refresh(self.frame)

        left_pupil_x = self.gazetracker.eye_left.pupil.x
        left_pupil_y = self.gazetracker.eye_left.pupil.y
        right_pupil_x = self.gazetracker.eye_right.pupil.x
        right_pupil_y = self.gazetracker.eye_right.pupil.y

        self.assertIsNotNone(left_pupil_y)
        self.assertIsNotNone(left_pupil_x)
        self.assertIsNotNone(right_pupil_y)
        self.assertIsNotNone(right_pupil_x)

if __name__ == "__main__":
    unittest.main()
