import re
import PySimpleGUI as sg
from capture import *
import win32gui

APP_NAME = "Webcamera Usability Testing"
APP_VERSION = "v0.1"
WINDOW_LIST = WindowCapture.get_window_names()


class Gui:
    THEME = "Dark"
    sg.theme(THEME)

    camera_feed = [[sg.Image(filename="", key="frame", size=(200, 200))]]

    window_feed = [[sg.Image(filename="", key="window", size=(200, 200))]]

    toggle = [
        [sg.Text("Turn webcam On/Off")],
        [
            sg.Button(
                "Off",
                size=(5, 1),
                button_color=("white", "red"),
                key="_TOGGLE_",
            )
        ],
    ]

    button_controls = [
        [sg.Text("Status:"), sg.Text("", key="status")],
        [sg.Button("Record"), sg.Button("Stop")],
    ]

    select_window = [
        [sg.Text("Current window:"), sg.Text("", key="current_window")],
        [
            sg.Combo(
                WINDOW_LIST,
                enable_events=True,
                readonly=True,
                font="Consolas 10",
                key="SELECT",
            )
        ],
        [sg.Button("Apply")],
    ]

    # TODO: add search bar and scrollbar
    left_col = [
        [sg.Text("Features", size=(25, 1))],
        [sg.Input(size=(25, 1), focus=False)],
        [sg.Checkbox("Generate Heatmap", default=False)],
        [sg.Checkbox("Show facial recognition", default=False)],
        [sg.Checkbox("Generate Heatmap", default=False)],
        [sg.Checkbox("Show facial recognition", default=False)],
        [sg.Checkbox("Show FPS", default=False)],
    ]
    right_col = [
        [sg.Column(camera_feed, justification="center")],
        [sg.Column(window_feed)],
        [
            sg.Column(button_controls),
            sg.Column(toggle),
            sg.Column(select_window),
        ],
    ]

    def __init__(self) -> None:
        self.layout = [
            [
                sg.Column(self.left_col),
                sg.VSeperator(),
                sg.Column(self.right_col),
            ]
        ]

        self.window = sg.Window(
            "{} {}".format(APP_NAME, APP_VERSION),
            self.layout,
            default_button_element_size=(12, 1),
            auto_size_buttons=False,
            resizable=True,
            element_justification="center",
            font="Helvetica 16",
        )
