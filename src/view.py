import io
import argparse

import pygetwindow

from camera import *
from gui import *
import pyautogui
from PIL import Image

from src.window import Window

IMG_SIZE_W = 100
IMG_SIZE_H = 100

test_cam = True


def main():
    device = args.camera
    gui = Gui()
    cam = Camera(device)
    _toggle = False
    window = Window("")
    titles_found = False

    while True:
        event, values = gui.window.read(timeout=10)
        if event == "Exit" or event == sg.WIN_CLOSED:
            return

        if not titles_found:
            titles_list = window.get_windows_titles_list()
            for title in titles_list:
                w = pygetwindow.getWindowsWithTitle(title)[0]
                if w.isMinimized:
                    titles_list.remove(title)
            gui.window["SELECT"].update(values=titles_list, visible=True)
            titles_found = True

        if event == "_TOGGLE_":
            _toggle = not _toggle
            gui.window.Element("_TOGGLE_").Update(
                ("Off", "On")[_toggle],
                button_color=(("white", ("red", "green")[_toggle])),
            )

            if _toggle:
                cam.is_recording = True
                gui.window["status"].update("Running")

            elif not _toggle:
                cam.is_recording = False
                gui.window["status"].update("Stopped")
                # img = np.full((IMG_SIZE_H, IMG_SIZE_W), 255)
                # TODO: "Kill" camera instance

        # Implement screen recording
        elif event == "Record":
            frame = pyautogui.getWindowsWithTitle(values["SELECT"])
            # frame = pyautogui.screenshot()
            # frame.save("test.png")
            # imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            # gui.window["frame"].update(data=imgbytes)

        elif event == "Stop":
            pass

        if cam.is_recording:
            if not test_cam:
                ret, frame = cam.capture.read()
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break

                imgbytes = cv2.imencode(".png", frame)[1].tobytes()
                gui.window["frame"].update(data=imgbytes)
            else:
                combo = values["SELECT"]
                window = Window(combo)
                path = "ressources/windowfeed/windowfeed.png"
                window.take_screenshot_of_window(path)
                img = Image.open("ressources/windowfeed/windowfeed.png")
                img.thumbnail((400, 400))
                bio = io.BytesIO()
                img.save(bio, format="PNG")
                gui.window["frame"].update(data=bio.getvalue())


if __name__ == "__main__":
    # Optional arguments if camera type is different from 0
    parser = argparse.ArgumentParser(description="webcam eye tracking.")
    parser.add_argument(
        "--camera", help="Camera divide number.", type=int, default=0
    )
    args = parser.parse_args()

    main()
