import pyautogui
import pygetwindow
from PIL import Image


class Window:
    def __init__(self, windowname : str):
        self.name = windowname

    def get_window(self):
        return pygetwindow.getWindowsWithTitle(self.name)[0]

    def get_windows_titles_list(self):
        return pygetwindow.getAllTitles()

    def take_screenshot_of_window(self, path : str):
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

