import PySimpleGUI as sg

APP_NAME = "Webcamera Usability Testing"
APP_VERSION = "v1.1"

search_icon = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABHElEQVQ4T2NkwA2YgFL/8MiDpRjRFAgD+aVALAvEv4GYFYj/A/EcID6AzTBkA9SACrqBuAqIryIp5gSyq4H4ExB3oRsCMwBk01ogjgPiDzicXQMUPw/EW5HlYQZEQ528Co+fQZYsBeIwbAaA/JgLxN/xGACSmgbElUD8EaYO5oLFQIFYAppB0k1AvACI76EbMAUoUA/EbwkYMhcon4PsUpgLXIGCmkA8CY8BAlB5UEDDAXI0LgOKNgPxdSyGgBIVyPZ+IL6EywCQDbOBeAsQrwDin1CFulDv6UENmI7LAJA4yKYQIPYEYmYovgOkQaHvC8QzgTgfiEFhBgboSRmL61GEUtANIdUAkGkohpBjAMiQTCA2BOI0cg2A+wsAV68vEVbw9/oAAAAASUVORK5CYII="


WINDOW_LIST = list()

dialogue = {
    0: "Please enter your desired webcam index (0=Internal, 1...X = External)!",
    1: "Choose webcam index",
    2: "Please enter your monitor size in inches!",
    3: "Monitor size",
    4: "Please calibrate before attempting to record!",
    5: "",
    6: "File not found!",
    7: "Look in the upper left corner and press 'Q' on your keyboard",
    8: "Look in the lower right corner and press 'W' on your keyboard",
    9: "Look at the left most side and press 'E' on your keyboard",
    10: "Look at the right most side and press 'R' on your keyboard",
}

exceptions = {
    0: "Please enter a valid integer number!",
    1: "Argument must be a real number, not 'NoneType'!"
}


class Gui:
    """
    GUI Class

    Used to execute the interface
    """

    def popup(self, message: str):
        sg.popup(message)

    @staticmethod
    def make_window():

        """
        Creates a window
        """
        THEME = "Dark Grey"
        HEADER_FONT = "Dosis 14 bold"
        DEFAULT_FONT = "Dosis 10"
        sg.theme(THEME)

        camera_feed = [[sg.Image(filename="", key="frame")]]

        window_feed = [[sg.Image(filename="", key="window")]]

        toggle = [
            [sg.Text("Webcam", font=HEADER_FONT)],
            [
                sg.Button(
                    "SHOW",
                    size=(12, 1),
                    button_color=("dark green", "grey44"),
                    key="_TOGGLE_",
                )
            ],
        ]

        button_controls = [
            [sg.Text("Status:", font=HEADER_FONT), sg.Text("Stopped", key="status")],
            [
                sg.Button(
                    "RECORD",
                    size=(8, 1),
                    button_color=("dark green", "grey44"),
                    key="_RECORDING_",
                )
            ],
        ]

        select_window = [
            [
                sg.Text("Current window:", font=HEADER_FONT),
                sg.Text("", key="current_window"),
            ],
            [
                sg.Combo(
                    "",
                    enable_events=True,
                    readonly=True,
                    font=DEFAULT_FONT,
                    key="SELECT",
                    size=(25, 1),
                ),
                sg.Button("Apply"),
            ],
        ]

        left_col = [
            [sg.Text("Features", size=(20, 1), font=HEADER_FONT)],
            [sg.Input(size=(25, 1), focus=False), sg.Image(search_icon)],
            [sg.Checkbox("Generate Heatmap", default=False, key="_HEATMAP_")],
            [sg.Checkbox("Left eye lines", default=False, key="_LELINES_")],
            [sg.Checkbox("Right eye lines", default=False, key="_RELINES_")],
            [sg.Checkbox("Show FPS", default=False, key="_FPS_")],
            [sg.Checkbox("Check if eyes are closed", default=False, key="_EYECLOSED_")],
            [sg.Checkbox("Outline Eyes", default=False, key="_OUTLINE_")],
            [sg.Checkbox("Ratio", default=False, key="_RATIO_")],
            [sg.Checkbox("Calculate Distance", default=False, key="_DISTANCE_")],
            [sg.Checkbox("New Approach", default=False, key="_NEWGAZE_")],
            [sg.Text("Screen size", size=(20, 1), font=DEFAULT_FONT, key="SIZETEXT")],
            [sg.Text("Upper bound", size=(20, 1), font=DEFAULT_FONT, key="UPPERBOUND")],
            [sg.Text("Lower bound", size=(20, 1), font=DEFAULT_FONT, key="LOWERBOUND")],
            [
                sg.Text(
                    "Rightmost bound", size=(20, 1), font=DEFAULT_FONT, key="RIGHTBOUND"
                )
            ],
            [
                sg.Text(
                    "Leftmost bound", size=(20, 1), font=DEFAULT_FONT, key="LEFTBOUND"
                )
            ],
        ]

        right_col = [
            [sg.Column(camera_feed, justification="center")],
            [sg.Column(window_feed)],
            [sg.Column(button_controls), sg.Column(toggle), sg.Column(select_window)],
        ]

        layout = [
            [sg.vtop(sg.Column(left_col)), sg.VSeperator(), sg.Column(right_col, justification="bottom")]
        ]

        window = sg.Window(
            "{} {}".format(APP_NAME, APP_VERSION),
            layout,
            finalize=True,
            default_button_element_size=(12, 1),
            auto_size_buttons=True,
            resizable=False,
            font=DEFAULT_FONT,
        )
        return window

    def __init__(self) -> None:
        self.window = self.make_window()
