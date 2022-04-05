import unittest
import os
import sys

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)

from src.gui import Gui

class TestGUI(unittest.TestCase):
    def test_gui(self):
        self.gui = Gui()
        self.assertFalse(self.gui.window.was_closed())
        self.gui.window.close()
        self.assertTrue(self.gui.window.was_closed())


if __name__ == "__main__":
    unittest.main()