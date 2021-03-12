import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


def survey(results, category_names, multiple_graphs=False):
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.set_xlim(0, np.sum(data, axis=1).max())

    category_colors = ["#a95aa1","#85c0f9","#f5793a","#0f2080", "#ee442f"]

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5,    
                label=colname, color=color)

        xcenters = starts + widths / 2
        if multiple_graphs:
            continue
        text_color = color
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            y_pos = pow(-1, i) * 0.28
            ax.text(x, y - y_pos, str(float(c)), ha='center', va='center',
                    color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')
    return fig, ax