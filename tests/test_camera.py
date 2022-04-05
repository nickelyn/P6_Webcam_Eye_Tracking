import platform
import unittest
import cv2 as cv


class TestCV(unittest.TestCase):
    def setUp(self):
        capture = cv.VideoCapture(0)
        self.seq = capture

    def test_camera(self):
        # TODO: Unable to test camera on VM. Check if actual user, if not dont run test
        if platform.system() == "Linux":
            return True

        self.assertTrue(self.seq.isOpened())
        self.seq.release()
        self.assertFalse(self.seq.isOpened())


if __name__ == "__main__":
    unittest.main()
