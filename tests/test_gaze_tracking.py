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

    def test_refresh_frame(self):
        self.gazetracker.refresh(self.frame)

        self.assertNotEqual(self.gazetracker.eye_left, None)
        self.assertNotEqual(self.gazetracker.eye_right, None)

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
        blinking = self.gazetracker.is_blinking()
        self.gazetracker.refresh(self.frame_closed)
        blinking_true = self.gazetracker.is_blinking()

        self.assertEqual(False, blinking)

    def test_ratios(self):
        self.gazetracker.refresh(self.frame)

        hor = self.gazetracker.hori_ratio()
        ver = self.gazetracker.vert_ratio()
        # If the pupils are located, the ratios will not be none
        self.assertIsNotNone(hor)
        self.assertIsNotNone(ver)


if __name__ == "__main__":
    unittest.main()
