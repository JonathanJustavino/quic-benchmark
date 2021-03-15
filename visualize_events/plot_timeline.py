import os
import re
import numpy as np
import matplotlib.pyplot as plt
from dataloader import load_results


def samples_path(samples_folder='samples'):
    folder_filter = 'quic-benchmark/visualize_events'
    dst_folder = os.getcwd()
    dst_folder = re.sub(folder_filter, "", dst_folder)
    return f"{dst_folder}{samples_folder}"


def set_timestamps():
    quic_key = "quic"
    tcp_key = "tcp"

    quic_keys = ["keylog", "session", "secure", "data", "streamEnd", "streamClose", "socketClose"]
    tcp_keys = ["keylog", "secure", "session", "data", "streamEnd", "streamClose", "socketClose"]

    quic_dict = load_results(quic_key, samples_path("samples_threshold5_dev2_delay0"))
    tcp_dict = load_results(tcp_key, samples_path("samples_threshold5_dev2_delay0"))    

    quic_labels, quic_stamps = get_timestamps(quic_dict, "session", quic_keys)
    tcp_labels, tcp_stamps = get_timestamps(tcp_dict, "keylog", tcp_keys)
    return quic_labels, quic_stamps, tcp_labels, tcp_stamps


def get_timestamps(dictionary, first_event, keys):
    average = "avg"
    stamps = []
    labels = [first_event]
    stamps.append(0)
    for key in keys:
        if key == first_event:
            continue
        value = round(dictionary["server"][f"{first_event}-to-{key}"][average] / 1000, 1)
        stamps.append(value)
        labels.append(key)
    return labels, stamps


quic_labels, quic_stamps, tcp_labels, tcp_stamps = set_timestamps()
event_name = []
vline_up = []
vline_down = []
for labels in quic_labels:
    event_name.append(0)

fig, axs = plt.subplots(2, 1, constrained_layout=True)
axs[0].plot(quic_stamps, event_name, marker="|", markersize=10)
axs[0].set_title('QUIC Event timeline')
axs[0].set_xlabel('Milliseconds')
axs[0].set_yticks([])
axs[0].set_xlim(left=None, right=48)

for i, (x_pos, label) in enumerate(zip(quic_stamps, quic_labels)):
    y_pos = pow(-1, i) * 0.015
    x_pos = x_pos - 0.8
    location = (x_pos, y_pos)
    axs[0].annotate(label, location)

axs[1].plot(tcp_stamps, event_name, marker="|", markersize=10)
axs[1].set_xlabel('Milliseconds')
axs[1].set_title('TCP/TLS Event timeline')
axs[1].set_yticks([])
axs[1].set_xlim(left=None, right=6)

for i, (x_pos, label) in enumerate(zip(tcp_stamps, tcp_labels)):
    y_pos = pow(-1, i) * 0.015
    x_pos = x_pos - 0.06
    location = (x_pos, y_pos)
    axs[1].annotate(label, location)

plt.show()