import unittest
from src.gaze_calculator.monitor_calculator import Monitor


class TestMonitorCalc(unittest.TestCase):
    def setUp(self):
        monitor = Monitor(diagonal=27)
        self.monitor = monitor

    def test_calculate_aspect_ration(self):
        # ARRANGE
        self.monitor.pixels_height = 1440
        self.monitor.pixels_width = 2560

        # ACT
        self.monitor.calculate_aspect_ratio()

        # ASSERT
        self.assertEqual(self.monitor.aspect_ratio, [16, 9], "Test")

    def test_convert_to_inches(self):
        # ARRANGE
        self.monitor.pixels_height = 1440
        self.monitor.pixels_width = 2560
        self.monitor.calculate_aspect_ratio()

        # ACT
        self.monitor.convert_pixels_to_size_inches()

        # ASSERT
        self.assertEqual(self.monitor.height, 13.237053470079092)
        self.assertEqual(self.monitor.width, 23.532539502362827)

    def test_size_to_cm(self):
        # ARRANGE
        self.monitor.pixels_height = 1440
        self.monitor.pixels_width = 2560
        self.monitor.calculate_aspect_ratio()
        self.monitor.convert_pixels_to_size_inches()

        # ACT
        self.monitor.size_to_cm()

        # ASSERT
        self.assertEqual(self.monitor.height, 33.6)
        self.assertEqual(self.monitor.width, 59.8)


if __name__ == "__main__":
    unittest.main()
