import os
import sys
import unittest

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)

from tests.test_window_title import *
from tests.test_boxes import *
from tests.test_camera import *
from tests.test_distance_detector import *
from tests.test_gaze_tracking import *
from tests.test_gui import *
from tests.test_monitor_calc import *

if __name__ == "__main__":
    unittest.main()
