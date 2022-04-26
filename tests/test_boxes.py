import unittest
from src.gaze_calculator.monitor_calculator import Monitor
from src.gaze_calculator.boxes import Box


class TestBoxes(unittest.TestCase):
    def setUp(self):
        monitor = Monitor(diagonal=27)
        monitor.pixels_height = 1440
        monitor.pixels_width = 2560
        monitor.calculate_aspect_ratio()
        monitor.convert_pixels_to_size_inches()
        monitor.size_to_cm()

        bounds = [1.0, 1.5, 1.0, 1.5]
        self.box = Box(monitor=monitor, bounds=bounds)

    def test_vertical_difference(self):
        self.assertEqual(self.box.ver_difference, self.box.lower - self.box.upper)

    def test_horizontal_difference(self):
        self.assertEqual(self.box.hor_difference, self.box.right - self.box.left)

    def test_box_amount(self):
        # Should result in 32 boxes on a 27inch 1440p monitor with 16:9 aspect ratio
        self.assertEqual(self.box.box_amount, 32)

    def test_actual_boxes(self):
        # ARRANGE
        ver_ratio = 1.5
        hor_ratio = 1.0

        # ACT
        actual = self.box.determine_actual_boxes(
            ver_ratio=ver_ratio, hor_ratio=hor_ratio
        )

        # ASSERT
        self.assertEqual(actual, [32, 32])


if __name__ == "__main__":
    unittest.main()
