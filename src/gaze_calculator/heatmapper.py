import numpy as np
import seaborn as sns
import matplotlib.pylab as plt


class Heatmap:
    def __init__(self, data: list, aspect_ratio: list):
        produce_heatmap(data, aspect_ratio)


def produce_heatmap(data: list, aspect: list):
    # TODO :  Needs to rezize the image, and should only show the values that are within the borders to the application chosen for the test
    plt.style.use("seaborn")
    plt.figure(figsize=(aspect[0], aspect[1]), dpi=80)
    heatmap = sns.heatmap(np.array(data), linewidth=1, annot=True)
    plt.title("Heatmap Using Seaborn Method")
    #plt.show()
    plt.savefig('ProducedHeatmap.png', dpi=1000)
