import math

from .monitor_calculator import Monitor


class Box:
    def __init__(self, monitor: Monitor, bounds: list):
        if monitor.aspect_ratio == [16, 9]:
            self.horizontal_bounds = 80
            self.vertical_bounds = 45
            self.box_amount = int(monitor.pixels_width / self.horizontal_bounds)
        elif monitor.aspect_ratio == [16, 10]:
            self.horizontal_bounds = 64
            self.vertical_bounds = 40
            self.box_amount = int(monitor.pixels_width / self.horizontal_bounds)
        else:
            print("Unknown ratio")

        self.upperx = bounds[0][0]
        self.uppery = bounds[0][1]
        self.lowerx = bounds[1][0]
        self.lowery = bounds[1][1]
        self.ver_difference = compare_vertical(self.uppery, self.lowery)
        self.hor_difference = compare_horizontal(self.lowerx, self.upperx)
        self.ver_box_index = self.ver_difference / self.box_amount
        self.hor_box_index = self.hor_difference / self.box_amount

    def determine_actual_boxes(self, xcoord, ycoord):
        if xcoord is None or ycoord is None:
            return None
        if ycoord < self.lowery:
            ycoord = self.lowery
        elif ycoord > self.uppery:
            ycoord = self.uppery

        vertical_box = (ycoord - self.lowery) / self.ver_box_index
        if vertical_box < 0:
            vertical_box = vertical_box * -1

        vertical_box = math.floor(vertical_box)

        if xcoord > self.upperx:
            xcoord = self.upperx
        elif xcoord < self.lowerx:
            xcoord = self.lowerx

        horizontal_box = (xcoord - self.lowerx) / self.hor_box_index
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
