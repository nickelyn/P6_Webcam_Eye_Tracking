import io
import os
import argparse
import pygetwindow
from camera import *
from gui import *
from capture import *
import pyautogui
from window import Window
from PIL import Image

IMG_SIZE_W = 400
IMG_SIZE_H = 400


def main():
    toggle = False
    window_capture = Window("")
    titles_found = False
    capture_window = False
    sentinel = 0

    # Event Loop
    while True:
        event, values = gui.window.read(timeout=50)

        if not titles_found:
            titles_list = window_capture.get_windows_titles_list()
            for title in titles_list:
                w = pygetwindow.getWindowsWithTitle(title)[0]
                # print(len(w.title))
                if w.isMinimized or len(title) == 0:
                    titles_list.remove(title)
            gui.window["SELECT"].update(values=titles_list, visible=True)
            titles_found = True

        if cam.is_recording:  # Only use features if camera is on

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
                cam.setsize(IMG_SIZE_W, IMG_SIZE_H)
                gui.window["status"].update("Running")
            elif not toggle:
                cam.is_recording = False
                gui.window["status"].update("Stopped")
                # TODO: Fix  opencv image size not correlating to numpy image size
                img = np.full((IMG_SIZE_H, IMG_SIZE_W), 255)
                imgbytes = cv2.imencode(".png", img)[1].tobytes()
                gui.window["frame"].update(data=imgbytes)

        if cam.is_recording:
            ret, frame = cam.capture.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            gui.window["window"].update(data=imgbytes)

        if capture_window:
            if sentinel > 20:
                combo = values["SELECT"]
                window = Window(combo)
                try:
                    dir = "resources/windowfeed/"
                    file_name = "windowfeed.png"
                    path = os.path.join(dir, file_name)
                    window.take_screenshot_of_window(path)
                    img = Image.open(path)
                    img.thumbnail((400, 400))
                    bio = io.BytesIO()
                    img.save(bio, format="PNG")
                    gui.window["frame"].update(data=bio.getvalue())
                    sentinel = 0
                except FileNotFoundError:
                    print("File not found")
                    os.makedirs(dir)
            sentinel += 1

        # TODO: Implement window capture
        elif event == "Record":
            frame = pyautogui.getWindowsWithTitle(values["SELECT"])
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

    main()
    # pyinstaller -c -F view.spec -y
