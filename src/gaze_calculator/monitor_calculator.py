import math

from screeninfo import get_monitors


class Monitor:
    def __init__(self, diagonal: int):
        self.height = 0
        self.width = 0
        self.aspect_ratio = 0
        self.pixels_width = 0
        self.pixels_height = 0
        self.aspect_ratio = list()
        self.diagonal = diagonal

    def calculate_aspect_ratio(self):
        ratio = self.pixels_width / self.pixels_height
        ratio = float("{:.2f}".format(ratio))
        if ratio == 1.78:
            self.aspect_ratio = [16, 9]
        elif ratio == 1.33:
            self.aspect_ratio = [4, 3]

    def get_monitor_dimension(self):
        monitors = get_monitors()
        for m in monitors:
            if m.is_primary:
                self.pixels_height = m.height
                self.pixels_width = m.width
                return

    def convert_pixels_to_size_inches(self):
        aspect_ratio = self.aspect_ratio[0] / self.aspect_ratio[1]
        aspect = aspect_ratio**2
        aspect = aspect + 1
        aspect = math.sqrt(aspect)
        self.height = self.diagonal / aspect
        self.width = aspect_ratio * self.height

    def size_to_cm(self):
        self.height = convert_inches_to_cm(self.height)
        self.width = convert_inches_to_cm(self.width)


def convert_inches_to_cm(value: float):
    cm = value * 2.54
    cm = float("{:.1f}".format(cm))
    return cm


if __name__ == "__main__":
    monitor = Monitor(27)
    monitor.get_monitor_dimension()
    monitor.calculate_aspect_ratio()
    monitor.convert_pixels_to_size_inches()
    monitor.size_to_cm()

    print(f"Height = {monitor.height}")
    print(f"Width = {monitor.width}")
