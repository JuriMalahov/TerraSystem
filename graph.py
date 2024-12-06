import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random

from matplotlib.ticker import FixedLocator

matplotlib.use('Qt5Agg')

x = np.array([i+1 for i in range(31)])
y = np.array([random.randint(0, 500) for _ in range(31)])

fig = plt.figure(figsize=(31, 4), num='Октябрь')
ax = fig.add_subplot()
fig.suptitle('Содержание урана в руде', fontsize=24)
ax.set_xlabel('Дата')
ax.set_ylabel('Содержание урана, в граммах')
ax.plot(x, y, marker='o', color='orange', linewidth=2)

ax.grid()
ax.xaxis.set_major_locator(FixedLocator([i for i in range(1, 32)]))
ax.yaxis.set_major_locator(FixedLocator([i for i in range(0, 500, 20)]))

plt.show()
