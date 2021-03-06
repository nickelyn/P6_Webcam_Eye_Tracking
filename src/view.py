import io
import os
import sys
import argparse

import pygetwindow
import pyautogui
from PIL import Image

from camera import *
from eyegaze import *
import gaze as gz
from gaze import Gaze
from gazetracker.gaze_tracking import GazeTracking
from gui import *
import platform as p
from window import Window

# Necessary to traverse up the directory tree
parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)

from definitions import *

IMG_SIZE_W = 400
IMG_SIZE_H = 400


def main():
    toggle = False
    window_capture = Window("")
    titles_found = False
    capture_window = False
    sentinel = 0
    gaze = Gaze()
    gaze.find_ref_image_width()
    new_gaze = GazeTracking()

    # Event Loop
    while True:
        event, values = gui.window.read(timeout=50)

        if not titles_found:
            titles_list = window_capture.get_windows_titles_list()
            if p.system() != "Darwin":
                for title in titles_list:
                    # TODO: Sometimes returns out of range error
                    w = pygetwindow.getWindowsWithTitle(title)[0]
                    # print(len(w.title))
                    if w.isMinimized or len(title) == 0:
                        titles_list.remove(title)
            gui.window["SELECT"].update(values=titles_list, visible=True)
            titles_found = True

        if cam.is_recording:  # Only use features if camera is on
            ret, frame = cam.capture.read()
            # if not ret:
            #    print("Can't receive frame (stream end?). Exiting ...")
            #    break
            gaze = gz.prepare_gaze_object(gaze, frame)
            # if values["_LELINES_"] or values["_RELINES_"]:
            # getFace(frame) OLD IMPLEMENTATION
            #    gz.handle_faces(
            #        gaze, frame, lle=values["_LELINES_"], lre=values["_RELINES_"]
            #    )
            gz.handle_faces(
                gaze,
                frame,
                lle=values["_LELINES_"],
                lre=values["_RELINES_"],
                closed=values["_EYECLOSED_"],
                outline=values["_OUTLINE_"],
                ratio=values["_RATIO_"],
                distance=values["_DISTANCE_"],
            )

            if values["_NEWGAZE_"]:
                new_gaze.refresh(frame)
                frame = new_gaze.annotated_frame()
                text = ""

                if new_gaze.is_blinking():
                    text = "Blinking"
                elif new_gaze.is_right():
                    text = "Looking right"
                elif new_gaze.is_left():
                    text = "Looking left"
                elif new_gaze.is_center():
                    text = "Looking center"

                cv2.putText(
                    frame,
                    str(new_gaze.vertical_ratio()),
                    (20, 20),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.5,
                    (147, 58, 31),
                    1,
                )
                cv2.putText(
                    frame,
                    str(new_gaze.horizontal_ratio()),
                    (40, 40),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.5,
                    (147, 58, 31),
                    1,
                )

            imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            gui.window["window"].update(data=imgbytes)

            # TODO: Implement features
            if values["_HEATMAP_"] == True:
                print("_HEATMAP_")

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
                cam.setsize(IMG_SIZE_W, IMG_SIZE_H)
                gui.window["status"].update("Running")
            elif not toggle:
                cam.is_recording = False
                gui.window["status"].update("Stopped")
                # TODO: Fix  opencv image size not correlating to numpy image size
                img = np.full((IMG_SIZE_H, IMG_SIZE_W), 255)
                imgbytes = cv2.imencode(".png", img)[1].tobytes()
                gui.window["window"].update(data=imgbytes)

        if capture_window:
            dir = os.path.join(RESOURCES_DIR, "windowfeed")
            file_name = "windowfeed.png"
            path = os.path.join(dir, file_name)
            if p.system() == "Darwin":  # TODO: Find different approach
                if sentinel > 50:
                    combo = values["SELECT"]
                    window = Window(combo)
                    try:
                        window.take_screenshot_of_window_mac(path)
                        img = Image.open(path)
                        img.thumbnail((200, 200))
                        bio = io.BytesIO()
                        img.save(bio, format="PNG")
                        gui.window["frame"].update(data=bio.getvalue())
                        sentinel = 0
                    except FileNotFoundError:
                        print("MacOS: File not found")
                        os.makedirs(dir)

                sentinel = sentinel + 1
            else:
                if sentinel > 20:
                    combo = values["SELECT"]
                    window = Window(combo)
                    try:
                        window.take_screenshot_of_window(path)
                        img = Image.open(path)
                        img.thumbnail((400, 400))  # TODO: Implement size scaling
                        bio = io.BytesIO()
                        img.save(bio, format="PNG")
                        gui.window["frame"].update(data=bio.getvalue())
                        sentinel = 0
                    except FileNotFoundError:
                        print("Windows: File not found")
                        os.makedirs(dir)
                sentinel += 1

        # TODO: Toggle off the Apply Event, otherwise the Record event cant be accessed
        elif event == "Record":
            frame = pyautogui.getWindowsWithTitle(values["SELECT"])
            gui.window.minimize()
            # frame = pyautogui.screenshot()
            # frame.save("test.png")
            # imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            # gui.window["frame"].update(data=imgbytes)

        elif event == "Apply":
            if capture_window:
                capture_window = False
            else:
                capture_window = True

        elif event == "Stop":
            pass

        if event == "Exit" or event == sg.WIN_CLOSED:
            gui.window.close()
            return


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
    # distance_detector = DistanceDetector()

    main()
    # pyinstaller -c -F view.spec -y
