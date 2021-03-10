import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from visualize_events.plot_timeplan import *
from visualize_events.dataloader import load_results


def samples_path(samples_folder='samples'):
    folder_filter = 'quic-benchmark'
    dst_folder = os.getcwd()
    dst_folder = re.sub(folder_filter, "", dst_folder)
    return f"{dst_folder}{samples_folder}"


def get_values(folder_name):
    quic_key = "quic"
    tcp_key = "tcp"

    quic_dict = load_results(quic_key, samples_path(folder_name))
    tcp_dict = load_results(tcp_key, samples_path(folder_name))

    session_key = "ready-to-session"
    handshake_key = "handshakeDuration"
    byte_key = "secure-to-data"
    transfer_key = "data-to-streamEnd"
    socket_key = "streamEnd-to-socketClose"

    quic_handshake = quic_dict[handshake_key]
    quic_byte = quic_dict['server'][byte_key]
    quic_transfer = quic_dict['server'][transfer_key]
    quic_socket = quic_dict['server'][socket_key]

    tcp_handshake = tcp_dict[handshake_key]
    tcp_byte = tcp_dict['server'][byte_key]
    tcp_transfer = tcp_dict['server'][transfer_key]
    tcp_socket = tcp_dict['server'][socket_key]

    convert_to_ms = lambda t: round((t / 1000), 1)
    quic_results = list(map(convert_to_ms, [quic_handshake, quic_byte, quic_transfer, quic_socket]))
    tcp_results = list(map(convert_to_ms, [tcp_handshake, tcp_byte, tcp_transfer, tcp_socket]))

    return quic_results, tcp_results


def plot_graph():
    category_names = ['Handshake', 'Time to first byte', 'Content Transfer', 'Close socket']
    del0_quic_results, del0_tcp_results = get_values("samples_threshold5_dev2_delay0")
    del10_quic_results, del10_tcp_results = get_values("samples_threshold5_dev2_delay0")
    del20_quic_results, del20_tcp_results = get_values("samples_threshold5_dev2_delay0")
    del60_quic_results, del60_tcp_results = get_values("samples_threshold5_dev2_delay0")

    results = {
        'QUIC (Delay 0)': del0_quic_results,
        'TCP/TLS (Delay 0)': del0_tcp_results,
        'QUIC (Delay 10)': del10_quic_results,
        'TCP/TLS (Delay 10)': del10_tcp_results,
        'QUIC (Delay 20)': del20_quic_results,
        'TCP/TLS (Delay 20)': del20_tcp_results,
        'QUIC (Delay 60)': del60_quic_results,
        'TCP/TLS (Delay 60)': del60_tcp_results,
    }
    survey(results, category_names)


if __name__ == '__main__':
    plot_graph()
    plt.xlabel("Milliseconds")
    plt.ylabel("Socket type")
    plt.show()