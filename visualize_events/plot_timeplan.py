import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


# def samples_path(samples_folder='samples'):
#     folder_filter = 'quic-benchmark/visualize-events'
#     dst_folder = os.getcwd()
#     dst_folder = re.sub(folder_filter, "", dst_folder)
#     return f"{dst_folder}"

# quic_key = "quic"
# tcp_key = "tcp"

# quic_dict = load_results(quic_key, samples_path())
# tcp_dict = load_results(tcp_key, samples_path())
# print(tcp_dict)

# session_key = "ready-to-session"
# handshake_key = "handshakeDuration"
# byte_key = "secure-to-data"
# transfer_key = "data-to-streamEnd"
# socket_key = "streamEnd-to-socketClose"

# quic_session = quic_dict[session_key] / 1000
# quic_handshake = quic_dict[handshake_key] / 1000
# quic_byte = quic_dict['server'][byte_key] / 1000
# quic_transfer = quic_dict['server'][transfer_key] / 1000
# quic_socket = quic_dict['server'][socket_key] / 1000

# tcp_session = tcp_dict[session_key] / 1000
# tcp_handshake = tcp_dict[handshake_key] / 1000
# tcp_byte = tcp_dict['server'][byte_key] / 1000
# tcp_transfer = tcp_dict['server'][transfer_key] / 1000
# tcp_socket = tcp_dict['server'][socket_key] / 1000

# category_names = ['Create session', 'Handshake', 'Time to first byte',
#                   'Content Transfer', 'Close socket']

# results = {
#     'QUIC': [quic_session, quic_handshake, quic_byte, quic_transfer, quic_socket],
#     'TCP/TLS': [tcp_session, tcp_handshake, tcp_byte, tcp_transfer, tcp_socket]
# }

def survey(results, category_names):
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

        text_color = 'white'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            ax.text(x, y, str(float(c)), ha='center', va='center',
                    color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')


    return fig, ax


# survey(results, category_names)
# plt.xlabel("Milliseconds")
# plt.ylabel("Socket type")
# plt.show()