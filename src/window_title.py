import pyautogui
import pygetwindow
from PIL import Image


class WindowTitle:
    def __init__(self, windowname: str):
        self.name = windowname
        self.point1 = None
        self.point2 = None

    def get_window(self):
        return pygetwindow.getWindowsWithTitle(self.name)[0]

    def get_titles_list(self):
        return pygetwindow.getAllTitles()

    def take_screenshot_of_window(self, path: str):
        window = pygetwindow.getWindowsWithTitle(self.name)[0]
        self.point1 = window.topleft
        self.point2 = window.bottomright

        pyautogui.screenshot(path)
        im = Image.open(path)
        im = im.crop((self.point1.x, self.point1.y, self.point2.x, self.point2.y))
        im.save(path)

    def take_screenshot_of_window_mac(self, path: str):
        x1, y1, width, height = pygetwindow.getWindowGeometry(self.name)
        x2 = x1 + width
        y2 = y1 + height
        pyautogui.screenshot(path)

        im = Image.open(path)
        im = im.crop((x1, y1 + 35, x2 + 570, y2))
        im.save(path)
