import os.path
import unittest
from src.distance_detection.distance_detector import *
import definitions as defs


class TestDistanceDetector(unittest.TestCase):
    def setUp(self):
        self.dd = DistanceDetector()
        self.ref_image_path = os.path.join(defs.DATA_DIR, "images/ref_image_new.jpg")

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
