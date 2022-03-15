import numpy as np
import cv2
import argparse
from camera import *
from gui import *
from capture import *
import pyautogui

IMG_SIZE_W = 100
IMG_SIZE_H = 100


def main():
    device = args.camera
    gui = Gui()

    _toggle = False

    while True:
        event, values = gui.window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            return

        if event == "_TOGGLE_":
            _toggle = not _toggle
            gui.window.Element("_TOGGLE_").Update(
                ("Off", "On")[_toggle],
                button_color=(("white", ("red", "green")[_toggle])),
            )

            if _toggle:
                cam = Camera(device)
                cam.is_recording = True
                gui.window["status"].update("Running")

            elif not _toggle:
                cam.is_recording = False
                gui.window["status"].update("Stopped")
                # img = np.full((IMG_SIZE_H, IMG_SIZE_W), 255)
                # TODO: "Kill" camera instance

            if cam.is_recording:
                ret, frame = cam.capture.read()
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break

                imgbytes = cv2.imencode(".png", frame)[1].tobytes()
                gui.window["frame"].update(data=imgbytes)
        # Implement screen recording
        elif event == "Record":
            frame = pyautogui.getWindowsWithTitle(values["SELECT"])
            # frame = pyautogui.screenshot()
            # frame.save("test.png")
            # imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            # gui.window["frame"].update(data=imgbytes)

        elif event == "Stop":
            pass


if __name__ == "__main__":
    # Optional arguments if camera type is different from 0
    parser = argparse.ArgumentParser(description="webcam eye tracking.")
    parser.add_argument(
        "--camera", help="Camera divide number.", type=int, default=0
    )
    args = parser.parse_args()

    main()
