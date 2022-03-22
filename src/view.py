import numpy as np
import cv2
import argparse
from camera import *
from gui import *
from capture import *
import pyautogui

IMG_SIZE_W = 400
IMG_SIZE_H = 400


def main():
    toggle = False

    # Event Loop
    while True:
        event, values = gui.window.read(timeout=50)

        if cam.is_recording: # Only use features if camera is on
            
            # TODO: Implement features    
            if values["_HEATMAP_"] == True:
                print("_HEATMAP_")

            if values["_FACIAL_RECOGNITION_"] == True:
                print("_FACIAL_RECOGNITION_")

            if values["_FPS_"] == True:
                print("_FPS_")

        if event == "_TOGGLE_":
            toggle = not toggle
            gui.window.Element("_TOGGLE_").Update(
                ("OFF", "ON")[toggle],
                button_color=(("white", ("red", "green")[toggle])),
            )
            if toggle:
                cam.is_recording = True
                cam.setsize(IMG_SIZE_W,IMG_SIZE_H)
                gui.window["status"].update("Running")
            elif not toggle:
                cam.is_recording = False
                gui.window["status"].update("Stopped")
                # TODO: Fix  opencv image size not correlating to numpy image size
                img = np.full((IMG_SIZE_H, IMG_SIZE_W), 255)
                imgbytes = cv2.imencode('.png', img)[1].tobytes()
                gui.window['frame'].update(data=imgbytes)

        if cam.is_recording:
            ret, frame = cam.capture.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            gui.window["frame"].update(data=imgbytes)

        # TODO: Implement window capture
        elif event == "Record":
            frame = pyautogui.getWindowsWithTitle(values["SELECT"])
            # frame = pyautogui.screenshot()
            # frame.save("test.png")
            # imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            # gui.window["frame"].update(data=imgbytes)

        elif event == "Stop":
            pass

        if event == "Exit" or event == sg.WIN_CLOSED:
            gui.window.close()
            exit(0)


if __name__ == "__main__":
    # Optional arguments if camera type is different from 0
    parser = argparse.ArgumentParser(description="webcam eye tracking.")
    parser.add_argument("--camera", help="Camera divide number.", type=int, default=0)
    args = parser.parse_args()

    # Store camera argument
    device = args.camera

    # Instantiate GUI and Camera Class
    gui = Gui()
    cam = Camera(device)

    main()
    # pyinstaller -c -F view.spec -y
