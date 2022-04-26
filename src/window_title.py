import pyautogui
import pygetwindow
from PIL import Image


class WindowTitle:
    def __init__(self, windowname: str):
        self.name = windowname

    def get_window(self):
        return pygetwindow.getWindowsWithTitle(self.name)[0]

    def get_titles_list(self):
        return pygetwindow.getAllTitles()

    def take_screenshot_of_window(self, path: str):
        window = pygetwindow.getWindowsWithTitle(self.name)[0]
        x0 = window.topleft
        height = window.height
        width = window.width
        x2 = x0.x + width
        y2 = x0.y + height

        pyautogui.screenshot(path)
        im = Image.open(path)
        im = im.crop((x0.x, x0.y, x2, y2))
        im.save(path)

    def take_screenshot_of_window_mac(self, path: str):
        x1, y1, width, height = pygetwindow.getWindowGeometry(self.name)
        x2 = x1 + width
        y2 = y1 + height
        pyautogui.screenshot(path)

        im = Image.open(path)
        im = im.crop((x1, y1 + 35, x2 + 570, y2))
        im.save(path)
