import numpy as np
import seaborn as sns
import matplotlib.pylab as plt


class Heatmap:
    def __init__(self, data: list, length: int):
        produce_heatmap(data, length)


def produce_heatmap(data: list, length: int):
    # TODO :  Needs to rezize the image, and should only show the values that are within the borders to the application chosen for the test
    plt.style.use("seaborn")
    plt.figure(figsize=(length, length))
    heatmap = sns.heatmap(np.array(data), linewidth=1, annot=True)
    plt.title("Heatmap Using Seaborn Method")
    plt.show()
