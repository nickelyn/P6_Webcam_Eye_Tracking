import numpy as np
import cv2
import argparse
import PySimpleGUI as sg
from camera import *

IMG_SIZE_W = 300
IMG_SIZE_H = 300


def main():
    sg.theme("darkteal11")

    # Define the window layout
    layout = [
        [sg.Text("Cam Demo", size=(100, 1), justification="center")],
        [sg.Image(filename="", key="frame", size=(600, 300))],
        [sg.Button("Record", size=(10, 1)), sg.Button("Stop", size=(10, 1))],
        [sg.Button("Exit", size=(16, 1), font="Helvetica 14")],
    ]

    window = sg.Window(
        "Demo", layout, element_justification="c", location=(800, 400)
    )

    # Event Loop #
    device = args.camera
    cam = Camera(device)

    while True:
        event, values = window.read(timeout=20)

        if event == "Exit" or event == sg.WIN_CLOSED:
            return

        elif event == "Record":
            cam.is_recording = True

        elif event == "Stop":
            cam.is_recording = False
            img = np.full((IMG_SIZE_H, IMG_SIZE_W), 255)

            imgbytes = cv2.imencode(".png", img)[1].tobytes()
            window["frame"].update(data=imgbytes)

        if cam.is_recording:
            ret, frame = cam.capture.read()

            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            window["frame"].update(data=imgbytes)


if __name__ == "__main__":

    # Optional arguments if camera type is different from 0
    parser = argparse.ArgumentParser(description="webcam eye tracking.")
    parser.add_argument(
        "--camera", help="Camera divide number.", type=int, default=0
    )
    args = parser.parse_args()
    main()
