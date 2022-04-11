from gaze_tracking import GazeTracking

def intialize_heatmap_array(box_amount : int):
    ha = []
    for i in range(box_amount):
        ha[i] = 0
    print(len(ha))
    return ha

if __name__ == "__main__":
    intialize_heatmap_array(32)
