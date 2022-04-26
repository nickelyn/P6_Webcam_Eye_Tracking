import unittest
import os
import sys
import platform as p

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)

from definitions import *
from src.window_title import WindowTitle


class TestWindow(unittest.TestCase):
    def setUp(self):
        self.window = WindowTitle("")
        self.assertFalse(os.path.exists(RESOURCES_DIR))
        os.makedirs(RESOURCES_DIR)
        self.assertTrue(os.path.exists(RESOURCES_DIR))

    def test_take_screenshot(self):
        file_name = "windowfeed.png"
        path = os.path.join(RESOURCES_DIR, file_name)
        if p.system() == "Darwin":
            self.window.take_screenshot_of_window_mac(path)
        else:
            self.window.take_screenshot_of_window(path)

        self.assertTrue(os.path.exists(path))

    def tearDown(self):
        self.assertTrue(os.path.exists(RESOURCES_DIR))
        os.remove(os.path.join(RESOURCES_DIR, "windowfeed.png"))
        os.rmdir(RESOURCES_DIR)
        self.assertFalse(os.path.exists(RESOURCES_DIR))


if __name__ == "__main__":
    unittest.main()
