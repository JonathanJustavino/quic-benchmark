import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from numpy.lib.twodim_base import _diag_dispatcher


def survey(results, category_names, multiple_graphs=False, split_threshold=20):
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = ["#a95aa1","#85c0f9","#f5793a","#0f2080", "#ee442f"]
    

    print(data)

    if should_split(data, split_threshold):
        length = 10
        socket_close_color = "#0f2080"

        start_socket_close = sum(data[0][0:-1])
        end_socket_close = sum(data[0])
        ax1_limit = start_socket_close + length
        ax2_start = end_socket_close - length
        figure, (ax, ax2) = plt.subplots(1, 2, sharey=True)

        set_xaxis_limit(ax, 0, ax1_limit)
        set_xaxis_limit(ax2, ax2_start, ax2_start + length*3)
        hide_axis_spine(ax, 'right')
        hide_axis_spine(ax2, 'left')

        ax = plot_it(ax, category_names, category_colors, data, data_cum, labels, multiple_graphs=multiple_graphs)
        ax2 = plot_split_handshake(ax2, ax2_start, length, socket_close_color, labels[0])
        set_xaxis_labels(ax, 'Milliseconds', 'left', (0.96, -0.07))
        set_xaxis_labels(ax2, '...', 'right', (-0.09, 0.5), size=20)
        ax.set_ylabel('Socket Type', loc='center', size=12)
        set_plot_labels(ax, ["QUIC", "TCP/TLS"])

        return figure, ax, ax2

    figure, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    return figure, plot_it(ax, category_names, category_colors, data, data_cum, labels, multiple_graphs=multiple_graphs)


def set_plot_labels(axis, labels):
    x_offset = -10
    axis.text(x_offset, 0, labels[0], ha='center', va='bottom')
    axis.text(x_offset, 1, labels[1], ha='center', va='bottom')


def set_xaxis_labels(axis, label, location, position, size=12):
    axis.set_xlabel(label, loc=location, size=size)
    axis.xaxis.set_label_coords(position[0], position[1])

def set_xaxis_limit(axis, start, end):
    axis.set_xlim(start, end)

def hide_axis_spine(axis, spine):
    axis.spines[spine].set_visible(False)


def should_split(data, split_threshold):
    last_left = data[0][-1:][0]
    last_right = data[1][-1:][0]
    return abs(last_left - last_right) > split_threshold

def plot_split_handshake(axis, starts, width, color, label):
    axis.barh(label, int(width), left=int(starts), height=0.5, color=color)
    axis.text(starts + width, 0.28, str(starts + width), ha='center', va='center', color=color)
    return axis

def plot_it(axis, category_names, category_colors, data, data_cum, labels, multiple_graphs=False):
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        axis.barh(labels, widths, left=starts, height=0.5, label=colname, color=color)

        xcenters = starts + widths / 2
        if multiple_graphs:
            continue
        text_color = color
        print(text_color)
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            y_pos = pow(-1, i) * 0.28
            axis.text(x, y - y_pos, str(float(c)), ha='center', va='center',
                    color=text_color)
    axis.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')
    return axis