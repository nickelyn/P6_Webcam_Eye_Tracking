import io
import os
import sys
import time

from gui import *
from PIL import Image
import keyboard as kb
import pygetwindow
import platform as p
import threading

from popup import PopUp
from camera import *
from gaze import Gaze
from gazetracker.gaze_tracking import GazeTracking
from gaze_calculator.monitor_calculator import Monitor
from gaze_calculator.boxes import Box
from gaze_calculator.heatmapper import Heatmap
from window_title import WindowTitle
from settings import Settings
from calibration.ninepoint import NinePointCalibrator
import gaze as gz

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
    titles_found = False
    capture_window = False
    initial_calibration = False
    sentinel = 0
    gaze = Gaze()
    gaze.find_ref_image_width()
    gaze_tracking = GazeTracking()
    calibration_iterations = 0
    calibration_popup = True
    calibration_array = []
    printer = True
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

        if not titles_found:
            titles_list = WindowTitle.get_titles_list()
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

                if not initial_calibration:
                    if calibration_popup:
                        gui.popup(dialogue.get(11))
                        calibration_popup = False
                    ninepoint = NinePointCalibrator(monitor=monitor)
                    if calibration_iterations != len(ninepoint.locations):
                        if ninepoint.window is None:
                            ninepoint.make_point(ninepoint.locations[calibration_iterations])
                            calibration_iterations = calibration_iterations + 1
                            calibration_array.append({f"left: {gaze_tracking.get_pupil_coords_left()}", f"right: {gaze_tracking.get_pupil_coords_right()}"})
                            threading.Timer(2.0, ninepoint.set_none())
                    else:
                        if printer:
                            print(calibration_array)
                            printer = False


                """
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
                            if (
                                actual_box is not None
                                and gaze_tracking.vert_ratio() is not None
                            ):
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
                            and gaze_tracking.vert_ratio() is not None
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
                            and gaze_tracking.vert_ratio() is not None
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
                        heatmap_array = intialise_heatmap_array(box.box_amount)
                        initial_calibration = True

                    gui.window["UPPERBOUND"].update(value=f"Upper bound = {upper_val}")
                    gui.window["LOWERBOUND"].update(value=f"Lower bound = {lower_val}")
                    gui.window["LEFTBOUND"].update(value=f"Leftmost bound = {left_val}")
                    gui.window["RIGHTBOUND"].update(
                        value=f"Rightmost bound = {right_val}"
                    )
                    """

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
        if event == "_RECORDING_":
            if not initial_calibration:
                gui.popup(dialogue.get(4))
            else:
                recording = not recording
                gui.window.Element("_RECORDING_").Update(  ##########X
                    ("RECORD", "STOP")[recording],
                    button_color=(("dark green", "red")[recording], "grey44"),
                )

                if generate_heatmap:
                    heatmap = Heatmap(
                        data=heatmap_array, monitor=monitor, name="ProducedHeatmap.png"
                    )
                    generate_heatmap = not generate_heatmap
                else:
                    heatmap_array = intialise_heatmap_array(box_amt=box.box_amount)
                    generate_heatmap = not generate_heatmap

        if event == "Apply":
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
        with open(CONFIG_DIR, "w") as configfile:
            settings.config.write(configfile)

    cam = Camera(device)

    main(monitor_size)
