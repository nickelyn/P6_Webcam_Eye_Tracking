import PySimpleGUI as sg


class PopUp:
    def make_window(self, name: str, title: str):
        layout = [[sg.Text(name)], [sg.InputText()], [sg.Submit(), sg.Cancel()]]
        window = sg.Window(title, layout)

        _, values = window.read()
        try:
            self.text_input = values[0]
            window.close()
        except KeyError:
            self.text_input = None

    def __init__(self, name: str, title: str):
        self.text_input = None
        self.make_window(name, title)