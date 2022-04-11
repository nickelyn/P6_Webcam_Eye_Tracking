import io
import os
import argparse
import time

import keyboard
import gaze_calculator.calibrator as cali
import pygetwindow
import gaze as gz

from gaze import Gaze
from camera import *
from gui import *
import pyautogui
from window import Window
from PIL import Image
from eyegaze import *
import platform as p
from gazetracker.gaze_tracking import GazeTracking
from gaze_calculator.monitor_calculator import Monitor
from gaze_calculator.boxes import Box
from gaze_calculator.heatmapper import Heatmap

IMG_SIZE_W = 400
IMG_SIZE_H = 400


def calibrate_monitor(screensize: int):
    monitor = Monitor(screensize)
    monitor.get_monitor_dimension()
    monitor.calculate_aspect_ratio()
    monitor.convert_pixels_to_size_inches()
    monitor.size_to_cm()

    return monitor


def intialize_heatmap_array(box_amount: int):
    ha = [[0 for x in range(box_amount + 1)] for i in range(box_amount + 1)]
    return ha


def main(screensize: int):
    toggle = False
    window_capture = Window("")
    titles_found = False
    capture_window = False
    initial_calibration = False
    sentinel = 0
    gaze = Gaze()
    gaze.find_ref_image_width()
    new_gaze = GazeTracking()
    upperleft = False
    lowerright = False
    rightmost = False
    leftmost = False
    uppervalue = 0
    lowervalue = 0
    rightvalue = 0
    leftvalue = 0
    monitor = calibrate_monitor(screensize)
    box = None
    recording = False
    heatmap_array = []
    generate_heatmap = False

    # Event Loop
    while True:
        event, values = gui.window.read(timeout=50)

        if not titles_found:
            titles_list = window_capture.get_windows_titles_list()
            if p.system() != "Darwin":
                for title in titles_list:
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

                if initial_calibration:
                    if recording:
                        if (
                            new_gaze.horizontal_ratio() is not None
                            and new_gaze.vertical_ratio() is not None
                        ):
                            # TODO : Upper right is scuffed, and lower right has a few spikes
                            actual_box = box.determine_actual_boxes(
                                ver_ratio=new_gaze.vertical_ratio(),
                                hor_ratio=new_gaze.horizontal_ratio(),
                            )
                            # print(actual_box)
                            vert_value = actual_box[0]
                            hori_value = actual_box[1]
                            # count the array up
                            heatmap_array[vert_value][hori_value] = (
                                heatmap_array[vert_value][hori_value] + 1
                            )
                        else:
                            print("got none")
                else:
                    # key = keyboard.is_pressed()
                    if upperleft is not True:
                        cv2.putText(
                            frame,
                            "Look in the upper left corner and pres 'Q' on your keyboard",
                            (20, 20),
                            cv2.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (147, 58, 31),
                            1,
                        )
                        if (
                            keyboard.is_pressed("q")
                            and new_gaze.vertical_ratio() is not None
                        ):
                            upperleft = True
                            uppervalue = float(
                                "{:.3f}".format(new_gaze.vertical_ratio())
                            )
                    elif lowerright is not True:
                        cv2.putText(
                            frame,
                            "Look in the lower right corner and pres 'W' on your keyboard",
                            (20, 20),
                            cv2.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (147, 58, 31),
                            1,
                        )
                        if (
                            keyboard.is_pressed("w")
                            and new_gaze.vertical_ratio() is not None
                        ):
                            lowerright = True
                            lowervalue = float(
                                "{:.3f}".format(new_gaze.vertical_ratio())
                            )

                    elif leftmost is not True:
                        cv2.putText(
                            frame,
                            "Look at the left most side and pres 'E' on your keyboard",
                            (20, 20),
                            cv2.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (147, 58, 31),
                            1,
                        )
                        if (
                            keyboard.is_pressed("e")
                            and new_gaze.horizontal_ratio() is not None
                        ):
                            leftmost = True
                            leftvalue = float(
                                "{:.3f}".format(new_gaze.horizontal_ratio())
                            )

                    elif rightmost is not True:
                        cv2.putText(
                            frame,
                            "Look at the right most side and pres 'R' on your keyboard",
                            (20, 20),
                            cv2.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (147, 58, 31),
                            1,
                        )
                        if (
                            keyboard.is_pressed("r")
                            and new_gaze.horizontal_ratio() is not None
                        ):
                            rightmost = True
                            rightvalue = float(
                                "{:.3f}".format(new_gaze.horizontal_ratio())
                            )

                    if upperleft and lowerright and rightmost and leftmost:
                        box = Box(
                            monitor=monitor,
                            bounds=[uppervalue, lowervalue, leftvalue, rightvalue],
                        )
                        # heatmap_array = intialize_heatmap_array(box_amount=box.box_amount)
                        initial_calibration = True

                    gui.window["UPPERBOUND"].update(value=f"Upper bound = {uppervalue}")
                    gui.window["LOWERBOUND"].update(value=f"Lower bound = {lowervalue}")
                    gui.window["LEFTBOUND"].update(
                        value=f"Leftmost bound = {leftvalue}"
                    )
                    gui.window["RIGHTBOUND"].update(
                        value=f"Rightmost bound = {rightvalue}"
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
                ("TOGGLE ON", "TOGGLE OFF")[toggle],
                button_color=((("dark green", "red")[toggle]), "grey44"),
            )
            gui.window["_NEWGAZE_"].update(value=toggle)
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
            if p.system() == "Darwin":  # TODO: Find different approach
                if sentinel > 50:
                    path = os.path.join(
                        os.getcwd(), "../resources/windowfeed/windowfeed.png"
                    )
                    combo = values["SELECT"]
                    window = Window(combo)
                    window.take_screenshot_of_window_mac(path)
                    img = Image.open(path)
                    img.thumbnail((200, 200))
                    bio = io.BytesIO()
                    img.save(bio, format="PNG")
                    gui.window["frame"].update(data=bio.getvalue())
                    sentinel = 0
                sentinel = sentinel + 1
            else:
                if sentinel > 20:
                    combo = values["SELECT"]
                    window = Window(combo)
                    dir = "resources/windowfeed/"
                    try:
                        file_name = "windowfeed.png"
                        path = os.path.join(dir, file_name)
                        window.take_screenshot_of_window(path)
                        img = Image.open(path)
                        img.thumbnail((400, 400))  # TODO: Implement size scaling
                        bio = io.BytesIO()
                        img.save(bio, format="PNG")
                        gui.window["frame"].update(data=bio.getvalue())
                        sentinel = 0
                    except FileNotFoundError:
                        print("File not found")
                        os.makedirs(dir)
                sentinel += 1

        # TODO: Toggle off the Apply Event, otherwise the Record event cant be accessed
        elif event == "_RECORDING_":
            # frame = pyautogui.getWindowsWithTitle(values["SELECT"])
            # gui.window.minimize()
            recording = not recording
            gui.window.Element("_RECORDING_").Update(
                ("RECORD", "STOP")[recording],
                button_color=((("dark green", "red")[recording], "grey44")),
            )

            if generate_heatmap:
                heatmap = Heatmap(data=heatmap_array, length=box.box_amount + 1)
                print(heatmap_array)
                generate_heatmap = not generate_heatmap
            else:
                heatmap_array = intialize_heatmap_array(box_amount=box.box_amount)
                generate_heatmap = not generate_heatmap

            # gui.window["_HEATMAP_"].update(value=recording)
            # frame = pyautogui.screenshot()
            # frame.save("test.png")
            # imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            # gui.window["frame"].update(data=imgbytes)

        elif event == "Apply":
            if capture_window:
                capture_window = False
            else:
                capture_window = True

        if event == "Exit" or event == sg.WIN_CLOSED:
            gui.window.close()
            return


if __name__ == "__main__":
    # Optional arguments if camera type is different from 0
    parser = argparse.ArgumentParser(description="webcam eye tracking.")
    parser.add_argument("--camera", help="Camera divide number.", type=int, default=0)
    parser.add_argument("--size", help="Screen size in inches.", type=int, default=0)
    args = parser.parse_args()

    if args.size == 0:
        print(
            "Please add your size of your monitor as an argument, before launching the system"
        )
        exit(1)

    # Store camera argument
    device = args.camera
    monitor_size = args.size

    # Instantiate GUI and Camera Class
    gui = Gui()
    cam = Camera(device)
    # distance_detector = DistanceDetector()

    gui.window["SIZETEXT"].update(value=f"Screen Size : {monitor_size} Inches")
    intialize_heatmap_array(32)

    main(monitor_size)

    # pyinstaller -c -F view.spec -y
