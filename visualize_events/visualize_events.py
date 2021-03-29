import os
import re
import numpy as np
import matplotlib.pyplot as plt
from dataloader import load_results

# Client events:
# ready, writeToServer, error
# Server events:
# listening, session, keylog, secure, data, streamEnd, streamClose, socketClose / handshakeDurationInNs


def samples_path(samples_folder='samples'):
    folder_filter = 'quic-benchmark/visualize_events'
    dst_folder = os.getcwd()
    dst_folder = re.sub(folder_filter, "", dst_folder)
    return f"{dst_folder}{samples_folder}"


def set_timestamps():
    quic_key = "quic"
    tcp_key = "tcp"

    quic_dict = load_results(quic_key, samples_path("samples_threshold5_dev2_delay0"))
    tcp_dict = load_results(tcp_key, samples_path("samples_threshold5_dev2_delay0"))    

    quic_labels, quic_stamps, quic_stdev = get_timestamps(quic_dict)
    tcp_labels, tcp_stamps, tcp_stdev = get_timestamps(tcp_dict)
    return quic_labels, quic_stamps, quic_stdev, tcp_labels, tcp_stamps, tcp_stdev


def get_timestamps(dictionary):
    average = "avg"
    secure = 'secure'
    keys = ["data", "streamEnd", "streamClose", "socketClose"]
    stamps = []
    labels = [secure]
    stdev_values = []
    stamps.append(0)
    stdev_values.append(0)
    for key in keys:
        value = round(dictionary["server"][f"{secure}-to-{key}"][average] / 1000, 1)
        value_stdev = round(dictionary["server"][f"{secure}-to-{key}"]["stdev"] / 1000, 1)
        stamps.append(value)
        labels.append(key)
        stdev_values.append(value_stdev)
    return labels, stamps, stdev_values


def annotate_points(subplot, stamps, labels, socket_type, color):
    # annotate each point on each graph
    for (x, y) in zip(stamps, labels):
        if socket_type == 'quic':
            subplot.annotate(x, (x, y), textcoords="offset points", xytext=(0, -15), ha='center', color=color)
        else:
            subplot.annotate(x, (x, y), textcoords="offset points", xytext=(0, 10), ha='center', color=color)



def plot_graph(quic_labels, quic_stamps, quic_stdev, tcp_labels, tcp_stamps, tcp_stdev):
    # static colors for graphs -> quic == blue, tcp == red
    quic_serv_col = 'b'
    col_tcp_serv = 'r'

    # init figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(np.array(tcp_stamps), np.array(tcp_labels), c=col_tcp_serv, marker='o', ls='', label="tcp server")
    ax.errorbar(np.array(tcp_stamps), np.array(tcp_labels), xerr=tcp_stdev, fmt='o', c=col_tcp_serv)
    ax.plot(np.array(quic_stamps), np.array(quic_labels), c=quic_serv_col, marker='o', ls='', label="quic server")
    ax.errorbar(np.array(quic_stamps), np.array(quic_labels), xerr=quic_stdev, fmt='o', c=quic_serv_col)
    annotate_points(ax, tcp_stamps, tcp_labels, 'tcp', col_tcp_serv)
    annotate_points(ax, quic_stamps, quic_labels, 'quic', quic_serv_col)

    plt.grid(1)
    plt.ylabel("Events of connection")
    plt.xlabel("Timeline in milliseconds")
    plt.legend(bbox_to_anchor=(-0.05, 1.2, 0.5, 0), loc="upper left", mode="expand", borderaxespad=3.5, ncol=2)
    plt.ylim([-0.5, 4.5])
    plt.show()


if __name__ == '__main__':
    quic_labels, quic_stamps, quic_stdev, tcp_labels, tcp_stamps, tcp_stdev = set_timestamps()
    plot_graph(quic_labels, quic_stamps, quic_stdev, tcp_labels, tcp_stamps, tcp_stdev)