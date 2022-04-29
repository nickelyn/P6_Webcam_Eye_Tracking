import configparser
import io
import sys
import argparse

import keyboard as kb
import pygetwindow
from gui import *
from PIL import Image
from popup import PopUp
from camera import *
from eyegaze import *
import gaze as gz
from gaze import Gaze
from gazetracker.gaze_tracking import GazeTracking
from gaze_calculator.monitor_calculator import Monitor
from gaze_calculator.boxes import Box
from gaze_calculator.heatmapper import Heatmap
import platform as p
from window_title import WindowTitle
from settings import Settings

# Necessary to traverse up the directory tree
parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)
from definitions import *

IMG_SIZE_W = 400
IMG_SIZE_H = 400


def calibrate_monitor(screen_size: int):
    monitor = Monitor(screen_size)
    monitor.get_monitor_dimension()
    monitor.calculate_aspect_ratio()
    monitor.convert_pixels_to_size_inches()
    monitor.size_to_cm()

    return monitor


def intialise_heatmap_array(box_amt: int):
    ha = [[0 for x in range(box_amt + 1)] for i in range(box_amt + 1)]
    return ha


def main(screen_size: int):
    toggle = False
    window_title = WindowTitle("")
    titles_found = False
    capture_window = False
    initial_calibration = False
    sentinel = 0
    gaze = Gaze()
    gaze.find_ref_image_width()
    gaze_tracking = GazeTracking()
    upper_left = False
    lower_right = False
    rightmost = False
    leftmost = False
    upper_val = 0
    lower_val = 0
    right_val = 0
    left_val = 0
    monitor = calibrate_monitor(screen_size)
    box = None
    recording = False
    heatmap_array = []
    generate_heatmap = False

    # Event Loop
    while True:
        event, values = gui.window.read(timeout=20)

        if titles_found:
            pass
        else:
            titles_list = window_title.get_titles_list()
            if p.system() != "Darwin":
                for title in titles_list:
                    # TODO: Sometimes returns out of range error
                    w = pygetwindow.getWindowsWithTitle(title)[0]
                    if w.isMinimized or len(title) == 0:
                        titles_list.remove(title)
            gui.window["SELECT"].update(values=titles_list, visible=True)
            titles_found = True

        if cam.is_recording:
            _, frame = cam.capture.read()

            gaze = gz.prepare_gaze_object(gaze, frame)
            gz.handle_faces(
                gaze,
                frame,
                lle=values[
                    "_LELINES_"
                ],  # TypeError: 'NoneType' object is not subscriptable
                lre=values["_RELINES_"],
                closed=values["_EYECLOSED_"],
                outline=values["_OUTLINE_"],
                ratio=values["_RATIO_"],
                distance=values["_DISTANCE_"],
            )

            if values["_NEWGAZE_"]:
                gaze_tracking.refresh(frame)
                frame = gaze_tracking.annotated_frame()
                text = ""

                if gaze_tracking.is_blinking():
                    text = "Blinking"
                elif gaze_tracking.is_right():
                    text = "Looking right"
                elif gaze_tracking.is_left():
                    text = "Looking left"
                elif gaze_tracking.is_center():
                    text = "Looking center"

                cv.putText(
                    frame,
                    str(gaze_tracking.vert_ratio()),
                    (20, 20),
                    cv.FONT_HERSHEY_DUPLEX,
                    0.5,
                    (147, 58, 31),
                    1,
                )
                cv.putText(
                    frame,
                    str(gaze_tracking.hori_ratio()),
                    (40, 40),
                    cv.FONT_HERSHEY_DUPLEX,
                    0.5,
                    (147, 58, 31),
                    1,
                )

                if initial_calibration:
                    if recording:
                        if (
                            gaze_tracking.hori_ratio() is None
                            and gaze_tracking.vert_ratio() is None
                        ):
                            return
                        else:
                            # TODO : Upper right is scuffed, and lower right has a few spikes
                            actual_box = box.determine_actual_boxes(
                                ver_ratio=gaze_tracking.vert_ratio(),
                                hor_ratio=gaze_tracking.hori_ratio(),
                            )
                            vert_val = actual_box[0]
                            hori_val = actual_box[1]
                            # count the array up
                            heatmap_array[vert_val][hori_val] = (
                                heatmap_array[vert_val][hori_val] + 1
                            )
                else:
                    if upper_left is not True:
                        cv.putText(
                            frame,
                            dialogue.get(7),
                            (20, 20),
                            cv.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (147, 58, 31),
                            1,
                        )
                        if (
                            kb.is_pressed("q")
                            and gaze_tracking.vert_ratio() is not None
                        ):
                            upper_left = True
                            upper_val = float(
                                "{:.3f}".format(gaze_tracking.vert_ratio())
                            )
                    elif lower_right is not True:
                        cv.putText(
                            frame,
                            dialogue.get(8),
                            (20, 20),
                            cv.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (147, 58, 31),
                            1,
                        )
                        if (
                            kb.is_pressed("w")
                            and gaze_tracking.vert_ratio() is not None
                        ):
                            lower_right = True
                            lower_val = float(
                                "{:.3f}".format(gaze_tracking.vert_ratio())
                            )

                    elif leftmost is not True:
                        cv.putText(
                            frame,
                            dialogue.get(9),
                            (20, 20),
                            cv.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (147, 58, 31),
                            1,
                        )
                        if (
                            kb.is_pressed("e")
                            and gaze_tracking.hori_ratio() is not None
                        ):
                            leftmost = True
                            left_val = float(
                                "{:.3f}".format(gaze_tracking.hori_ratio())
                            )

                    elif rightmost is not True:
                        cv.putText(
                            frame,
                            dialogue.get(10),
                            (20, 20),
                            cv.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (147, 58, 31),
                            1,
                        )
                        if (
                            kb.is_pressed("r")
                            and gaze_tracking.hori_ratio() is not None
                        ):
                            rightmost = True
                            right_val = float(
                                "{:.3f}".format(gaze_tracking.hori_ratio())
                            )

                    if upper_left and lower_right and rightmost and leftmost:
                        box = Box(
                            monitor=monitor,
                            bounds=[upper_val, lower_val, left_val, right_val],
                        )
                        initial_calibration = True

                    gui.window["UPPERBOUND"].update(value=f"Upper bound = {upper_val}")
                    gui.window["LOWERBOUND"].update(value=f"Lower bound = {lower_val}")
                    gui.window["LEFTBOUND"].update(value=f"Leftmost bound = {left_val}")
                    gui.window["RIGHTBOUND"].update(
                        value=f"Rightmost bound = {right_val}"
                    )

            imgbytes = cv.imencode(".png", frame)[1].tobytes()
            gui.window["window"].update(data=imgbytes)

        if event == "_TOGGLE_":
            toggle = not toggle
            gui.window.Element("_TOGGLE_").Update(
                ("SHOW", "HIDE")[toggle],
                button_color=(("white", ("green", "red")[toggle])),
            )
            if toggle:
                cam.is_recording = True
                cam.setsize(IMG_SIZE_W, IMG_SIZE_H)

            elif not toggle:
                cam.is_recording = False

        if capture_window:
            dir = os.path.join(RESOURCES_DIR, "windowfeed")
            file_name = "windowfeed.png"
            path = os.path.join(dir, file_name)
            if get_OS == "Darwin":
                if sentinel > 50:
                    combo = values["SELECT"]
                    window = WindowTitle(combo)
                    try:
                        window.take_screenshot_of_window_mac(path)
                        img = Image.open(path)
                        img.thumbnail((200, 200))
                        bio = io.BytesIO()
                        img.save(bio, format="PNG")
                        gui.window["frame"].update(data=bio.getvalue())
                        sentinel = 0
                    except FileNotFoundError:
                        print(f"MacOS: {dialogue.get(6)}")
                        os.makedirs(dir)

                sentinel = sentinel + 1
            else:
                if sentinel > 20:
                    combo = values["SELECT"]
                    window = WindowTitle(combo)
                    try:
                        path = os.path.join(dir, file_name)
                        window.take_screenshot_of_window(path)
                        img = Image.open(path)
                        img.thumbnail((400, 400))  # TODO: Implement size scaling
                        bio = io.BytesIO()
                        img.save(bio, format="PNG")
                        gui.window["frame"].update(data=bio.getvalue())
                        sentinel = 0
                    except FileNotFoundError:
                        print(f"Windows: {dialogue.get(6)}")
                        os.makedirs(dir)
                sentinel += 1

        # TODO: Toggle off the Apply Event, otherwise the Record event cant be accessed
        elif event == "_RECORDING_":
            if not initial_calibration:
                gui.popup(dialogue.get(4))
            else:
                recording = not recording
                gui.window.Element("_RECORDING_").Update(
                    ("RECORD", "STOP")[recording],
                    button_color=(("dark green", "red")[recording], "grey44"),
                )

                if generate_heatmap:
                    heatmap = Heatmap(data=heatmap_array, length=box.box_amount + 1)
                    print(heatmap_array)
                    generate_heatmap = not generate_heatmap
                else:
                    heatmap_array = intialise_heatmap_array(box_amt=box.box_amount)
                    generate_heatmap = not generate_heatmap

        elif event == "Apply":
            if capture_window:
                capture_window = False
            else:
                capture_window = True

        if event in (sg.WIN_CLOSED, "Quit"):
            gui.window.close()
            return


if __name__ == "__main__":
    gui = Gui()
    settings = Settings()

    # TODO: Check for illegal input.
    if settings.config.has_option("SETTINGS", "monitor_size"):
        monitor_size = int(settings.get_setting("SETTINGS", "monitor_size"))
    if settings.config.has_option("SETTINGS", "camera_type"):
        device = int(settings.get_setting("SETTINGS", "camera_type"))
    else:
        while True:
            try:
                popup = PopUp(dialogue.get(0), dialogue.get(1))
                device = int(popup.text_input)
                popup = PopUp(dialogue.get(2), dialogue.get(3))
                monitor_size = int(popup.text_input)
                break
            except ValueError:
                gui.popup(exceptions.get(0))
            except TypeError:
                gui.popup(exceptions.get(1))
        settings.config["SETTINGS"]["camera_type"] = str(device)
        settings.config["SETTINGS"]["monitor_size"] = str(monitor_size)
        # TODO: Possible file permissions error when bundled.
        with open("settings.cfg", "w") as configfile:
            settings.config.write(configfile)

    gui.window["SIZETEXT"].update(f"Screen size: {monitor_size} inches")
    cam = Camera(device)
    # intialise_heatmap_array(32)

    main(monitor_size)
