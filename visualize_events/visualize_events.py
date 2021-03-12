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


# def get_values(folder_name):
def set_timestamps():
    quic_key = "quic"
    tcp_key = "tcp"

    quic_dict = load_results(quic_key, samples_path("samples_threshold5_dev2_delay0"))
    tcp_dict = load_results(tcp_key, samples_path("samples_threshold5_dev2_delay0"))    

    quic_labels, quic_stamps = get_timestamps(quic_dict)
    tcp_labels, tcp_stamps = get_timestamps(tcp_dict)
    return quic_labels, quic_stamps, tcp_labels, tcp_stamps


def get_timestamps(dictionary):
    average = "avg"
    secure = 'secure'
    keys = ["data", "streamEnd", "streamClose", "socketClose"]
    stamps = []
    labels = [secure]
    stamps.append(0)
    for key in keys:
        value = round(dictionary["server"][f"{secure}-to-{key}"][average] / 1000, 1)
        stamps.append(value)
        labels.append(key)
    return labels, stamps


def annotate_points(subplot, stamps, labels, socket_type, color):
    # annotate each point on each graph
    for (x, y) in zip(stamps, labels):
        if socket_type == 'quic':
            subplot.annotate(x, (x, y), textcoords="offset points", xytext=(0, 10), ha='center', color=color)
        else:
            subplot.annotate(x, (x, y), textcoords="offset points", xytext=(0, -15), ha='center', color=color)



def plot_graph(quic_labels, quic_stamps, tcp_labels, tcp_stamps):
    # static colors for graphs -> quic == blue, tcp == red
    quic_serv_col = 'b'
    col_tcp_serv = 'r'

    # init figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(np.array(tcp_stamps), np.array(tcp_labels), c=col_tcp_serv, marker='o', ls='', label="tcp server")
    ax.plot(np.array(quic_stamps), np.array(quic_labels), c=quic_serv_col, marker='o', ls='', label="quic server")
    annotate_points(ax, tcp_stamps, tcp_labels, 'tcp', col_tcp_serv)
    annotate_points(ax, quic_stamps, quic_labels, 'quic', quic_serv_col)

    plt.grid(1)
    plt.xlabel("Events of connection")
    plt.ylabel("Timeline in milliseconds")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    quic_labels, quic_stamps, tcp_labels, tcp_stamps = set_timestamps()
    plot_graph(quic_labels, quic_stamps, tcp_labels, tcp_stamps)