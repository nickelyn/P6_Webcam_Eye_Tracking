import os
import sys
import platform
import random
import unittest
import glob
import numpy as np
import cv2 as cv
import logging

# TODO: Unable to test camera on VM. Check if actual user, if not dont run test
class TestCV(unittest.TestCase):
    def setUp(self):
        capture = cv.VideoCapture(0)
        self.seq = capture

    def test_camera(self):
        log = logging.getLogger(__class__.__name__)
        if platform.system() == "Linux":
            log.debug(platform.system())
            print(platform.system())
            return True
        log.debug("Testing camera")
        log.debug(platform.system())
        self.assertTrue(self.seq.isOpened())
        self.seq.release()
        self.assertFalse(self.seq.isOpened())


if __name__ == "__main__":
    unittest.main()
