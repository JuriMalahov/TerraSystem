import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random

from matplotlib.ticker import FixedLocator


def show_graph(umass_list):
    matplotlib.use('Qt5Agg')

    x = np.array([i + 1 for i in range(len(umass_list))])
    y = np.array([])
    for i in umass_list:
        y = np.append(y, int(i[0]))

    fig = plt.figure(figsize=(31, 4), num='Октябрь')
    ax = fig.add_subplot()
    fig.suptitle('Дневная добыча урана', fontsize=24)
    ax.set_xlabel('Дата')
    ax.set_ylabel('Содержание урана, в граммах')
    ax.plot(x, y, marker='o', color='orange', linewidth=2)

    ax.grid()
    ax.xaxis.set_major_locator(FixedLocator([i for i in range(1, 32)]))
    ax.yaxis.set_major_locator(FixedLocator([i for i in range(0, 500, 20)]))

    plt.show()
