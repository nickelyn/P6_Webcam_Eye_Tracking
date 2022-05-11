import PySimpleGUI as sg

class Loading:
    def make_window(self, stage_txt: str):
        THEME = "Dark Grey"
        layout = [[sg.Text(stage_txt)]]
        sg.theme(THEME)

        window = sg.Window("Loading", layout, size=(290, 50), keep_on_top=True)

        self.window = window


    def __init__(self, stage: str):
        self.window = None
        self.make_window(stage)