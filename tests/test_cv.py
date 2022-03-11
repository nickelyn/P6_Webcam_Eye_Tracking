import random
import unittest
import glob
import numpy as np
import cv2 as cv


class TestCV(unittest.TestCase):
    def setUp(self):
        capture = cv.VideoCapture(0)
        self.seq = capture

    def test_camera(self):
        self.assertTrue(self.seq.isOpened())


if __name__ == "__main__":
    unittest.main()
