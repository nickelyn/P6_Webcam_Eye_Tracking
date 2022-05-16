from gazetracker.gaze_tracking import GazeTracking
from gaze_calculator.monitor_calculator import Monitor
from gaze_calculator.boxes import Box
from gaze_calculator.heatmapper import Heatmap
from definitions import *
import cv2 as cv
from tqdm import tqdm

SCREEN_SIZE = 27
DIMENSIONS = [2560, 1440]
UPPER = 1.183
LOWER = 1.5
RIGHT = 0.6
LEFT = 0.917
VIDEO_PATH = os.path.join(DATA_DIR, "videos/benchmark-video.mp4")


def _calibrate_monitor(screen_size: int):
    monitor = Monitor(screen_size)
    monitor.pixels_height = 1440
    monitor.pixels_width = 2560
    monitor.calculate_aspect_ratio()
    monitor.convert_pixels_to_size_inches()
    monitor.size_to_cm()

    return monitor


def intialise_heatmap_array(box_amt: int):
    ha = [[0 for x in range(box_amt + 1)] for i in range(box_amt + 1)]
    return ha


def _benchmark():
    gaze_tracking = GazeTracking()
    monitor = _calibrate_monitor(SCREEN_SIZE)

    cap = cv.VideoCapture(VIDEO_PATH)

    video_length = int(cap.get(cv.CAP_PROP_FRAME_COUNT)) - 1
    print("Number of frames: ", video_length)
    count = 0
    box = Box(monitor=monitor, bounds=[UPPER, LOWER, LEFT, RIGHT])
    heatmap_array = intialise_heatmap_array(box_amt=box.box_amount)
    print("Started processing")
    pbar = tqdm(total=video_length)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
        gaze_tracking.refresh(frame)
        frame = gaze_tracking.annotated_frame()
        if gaze_tracking.hori_ratio() is None and gaze_tracking.vert_ratio() is None:
            continue
        actual_box = box.determine_actual_boxes(
            ver_ratio=gaze_tracking.vert_ratio(), hor_ratio=gaze_tracking.hori_ratio()
        )
        if actual_box is not None:
            vert_val = actual_box[0]
            hori_val = actual_box[1]
            # count the array up
            heatmap_array[vert_val][hori_val] = heatmap_array[vert_val][hori_val] + 1
        count = count + 1
        pbar.update(1)
        if count > (video_length - 1):
            cap.release()
            break

    pbar.close()
    Heatmap(data=heatmap_array, monitor=monitor, name="BenchmarkHeatmap.png")
    print("Finished processing, heatmap generated")


if __name__ == "__main__":
    _benchmark()
