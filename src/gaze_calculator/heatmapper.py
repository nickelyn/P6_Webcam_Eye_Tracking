import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
from src.gaze_calculator.monitor_calculator import Monitor


class Heatmap:
    def __init__(self, data: list, monitor: Monitor, name: str):
        produce_heatmap(data, monitor, name)


def produce_heatmap(data: list, monitor: Monitor, name: str):
    # TODO :  Needs to rezize the image, and should only show the values that are within the borders to the application chosen for the test
    plt.style.use("seaborn")
    plt.figure(figsize=(monitor.aspect_ratio[0], monitor.aspect_ratio[1]), dpi=80)
    heatmap = sns.heatmap(np.array(data), linewidth=1, annot=True)
    plt.title("Heatmap Using Seaborn Method")
    # plt.show()
    dpi = int(monitor.pixels_height / monitor.aspect_ratio[1])
    plt.savefig(name, dpi=dpi)
