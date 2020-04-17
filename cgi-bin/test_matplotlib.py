#!C:\BeelineProgFiles\python\python.exe
print("Content-Type: image/png\n\n")
print()



from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
Figure(figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')

import numpy as np


import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Fixing random state for reproducibility
np.random.seed(19680801)


def make_fig():
    """
    Make a figure and save it to "webagg.png".

    """
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.plot([1, 2, 3], 'ro--', markersize=12, markerfacecolor='g')

    # make a translucent scatter collection
    x = np.random.rand(100)
    y = np.random.rand(100)
    area = np.pi * (10 * np.random.rand(100)) ** 2  # 0 to 10 point radii
    c = ax.scatter(x, y, area)
    c.set_alpha(0.5)

    # add some text decoration
    ax.set_title('My first image')
    ax.set_ylabel('Some numbers')
    ax.set_xticks((.2, .4, .6, .8))
    labels = ax.set_xticklabels(('Bill', 'Fred', 'Ted', 'Ed'))

    # To set object properties, you can either iterate over the
    # objects manually, or define you own set command, as in setapi
    # above.
    for label in labels:
        label.set_rotation(45)
        label.set_fontsize(12)

    FigureCanvasAgg(fig).print_png('webapp.png', dpi=150)
    img = mpimg.imread('webapp.png')
    plt.imshow(img)




make_fig()