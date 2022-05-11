import math

from .monitor_calculator import Monitor


class Box:
    def __init__(self, monitor: Monitor, bounds: list):
        if monitor.aspect_ratio == [16, 9]:
            self.horizontal_bounds = 80
            self.vertical_bounds = 45
            self.box_amount = int(monitor.pixels_width / self.horizontal_bounds)
        else:
            print("Unknown ratio")

        self.upper = bounds[0]
        self.lower = bounds[1]
        self.left = bounds[2]
        self.right = bounds[3]
        self.ver_difference = compare_vertical(self.upper, self.lower)
        self.hor_difference = compare_horizontal(self.left, self.right)
        self.ver_box_index = self.ver_difference / self.box_amount
        self.hor_box_index = self.hor_difference / self.box_amount

    def determine_actual_boxes(self, ver_ratio, hor_ratio):
        if ver_ratio is None or hor_ratio is None:
            return None
        if ver_ratio > self.lower:
            ver_ratio = self.lower
        elif ver_ratio < self.upper:
            ver_ratio = self.upper

        vertical_box = (ver_ratio - self.upper) / self.ver_box_index
        if vertical_box < 0:
            vertical_box = vertical_box * -1

        vertical_box = math.floor(vertical_box)

        if hor_ratio > self.left:
            hor_ratio = self.left
        elif hor_ratio < self.right:
            hor_ratio = self.right

        horizontal_box = (hor_ratio - self.right) / self.hor_box_index
        if horizontal_box < 0:
            horizontal_box = horizontal_box * -1
        horizontal_box = math.floor(horizontal_box)

        return [vertical_box, int(self.box_amount - horizontal_box)]


def compare_vertical(upper: float, lower: float):
    if upper > lower:
        return upper - lower
    return lower - upper


def compare_horizontal(left: float, right: float):
    if left > right:
        return left - right
    return right - left
