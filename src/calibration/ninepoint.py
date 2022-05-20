import PySimpleGUI as sg
from src.gaze_calculator.monitor_calculator import Monitor

IMG_SIZE = (30, 30)
THEME = "Dark Grey"
b64_string = b"iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAeGVYSWZNTQAqAAAACAAFARIAAwAAAAEAAQAAARoABQAAAAEAAABKARsABQAAAAEAAABSASgAAwAAAAEAAgAAh2kABAAAAAEAAABaAAAAAAAAAEgAAAABAAAASAAAAAEAAqACAAQAAAABAAAAHqADAAQAAAABAAAAHgAAAAB2s9K0AAAACXBIWXMAAAsTAAALEwEAmpwYAAABWWlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNi4wLjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgoZXuEHAAABeElEQVRIDe1WQU7DMBCctBER3+CCxJk7B34DR/qAvIc/cOgnkLj0G6hS0zBjea3aSUhtQEKQlaL1Ojszu5uqNvDfrEobboHVDVBfAX36riTeAdUrcCDvcRJPpUEhk8mZL1Lu2vAtO6Xq8Ra4vgPuL4H9gYWsLCHTqz2S9+9AswVeyP0mDT5x58/AhbifgAdW1+thhvMW5/hTrDjFbRpah47tm6pTvaDtWeWani7fCGKd6Pg0xmkaYgvCCmQarxASZdXrr4xaWHGJky6ygbCSfVZlPkKcGRDr6hfHWPFje4HaC4c4ZzGH/VQ4Ryg3dxHOnVhx/jLq4tHlApdR506sOP93jlr/8qU2hx2cTroeuGOFznyJuGHlxZnaQJgbvT9ZOv8d5g6alNPFxEqzI7gWZ5oUhHf+GNYdySc1vuoUc1bssY7fOE1DBEFYV1BtbHkx2wCP333ZE7dpaB0Zqywaa0QyEaTcoWPlU7Vvf+hCT+6x39hEmX9x+wMjMnf+L6GI4wAAAABJRU5ErkJggg=="


class NinePointCalibrator:
    def __init__(self, monitor: Monitor):
        self.window = None
        self.locations = [
            (0, 0),
            (monitor.pixels_width / 2, 0),
            (monitor.pixels_width, 0),
            (0, monitor.pixels_height / 2),
            (monitor.pixels_width / 2, monitor.pixels_height / 2),
            (monitor.pixels_width, monitor.pixels_height / 2),
            (0, monitor.pixels_height),
            (monitor.pixels_width / 2, monitor.pixels_height),
            (monitor.pixels_width, monitor.pixels_height),
        ]
        """
        for i in range(0, len(self.locations)):
            print(self.locations[i])
            self.make_point(self.locations[i])
        """
    def make_point(self, location):
        layout = [
            [
                sg.Button(
                    "", image_data=b64_string, border_width=0, key="Exit", size=(1, 1)
                )
            ]
        ]
        sg.theme(THEME)
        self.window = sg.Window(
            "Window Title", layout, location=location, margins=(0, 0), finalize=True
        )
        self.window.read()


    def set_none(self):
        self.window.close()
        self.window = None


def _calibrate_monitor(screen_size: int):
    monitor = Monitor(screen_size)
    monitor.get_monitor_dimension()
    monitor.calculate_aspect_ratio()
    monitor.convert_pixels_to_size_inches()
    monitor.size_to_cm()

    return monitor


if __name__ == "__main__":
    monitor = _calibrate_monitor(16)
    cal = NinePointCalibrator(monitor)
