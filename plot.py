import os
import re
import statistics as stat
import matplotlib.pyplot as plt
from visualize_events.plot_timeplan import *
from visualize_events.dataloader import load_results


def convert_to_ms(value):
    return round((value / 1000), 1)


def samples_path(samples_folder='samples'):
    dst_folder = os.getcwd()
    return f"{dst_folder}/samples/{samples_folder}"


def get_avg_values(folder_name):
    quic_key = "quic"
    tcp_key = "tcp"

    quic_dict = load_results(quic_key, samples_path(folder_name))
    tcp_dict = load_results(tcp_key, samples_path(folder_name))

    handshake_key = "handshakeDuration"
    byte_key = "secure-to-data"
    transfer_key = "data-to-streamEnd"
    socket_key = "streamEnd-to-socketClose"
    average = "avg"

    quic_handshake = quic_dict[handshake_key][average]
    quic_byte = quic_dict['server'][byte_key][average]
    quic_transfer = quic_dict['server'][transfer_key][average]
    quic_socket = quic_dict['server'][socket_key][average]

    tcp_handshake = tcp_dict[handshake_key][average]
    tcp_byte = tcp_dict['server'][byte_key][average]
    tcp_transfer = tcp_dict['server'][transfer_key][average]
    tcp_socket = tcp_dict['server'][socket_key][average]

    quic_results = list(map(convert_to_ms, [quic_handshake, quic_byte, quic_transfer, quic_socket]))
    tcp_results = list(map(convert_to_ms, [tcp_handshake, tcp_byte, tcp_transfer, tcp_socket]))

    return quic_results, tcp_results


def apply_func_to_values(dictionary, func, round_by):
    server = 'server'
    client = 'client'
    hs = 'handshakeDuration'
    func_name = func.__name__
    results = {func_name: {'server': {}, 'client': {}, 'handshake': {}}}

    for event in dictionary[server]:
        results[func_name][server][event] = round(func(dictionary[server][event].values()), round_by)

    for event in dictionary[client]:
        results[func_name][client][event] = round(func(dictionary[client][event].values()), round_by)

    results[func_name]['handshake'] = round(func(dictionary[hs].values()), round_by)
    return results


def get_value_stats(folder_name, statistic_func=None, round_by=2):
    if not statistic_func:
        print("No statistical function provided")
        return None
    quic_key = "quic"
    tcp_key = "tcp"

    quic_dict = load_results(quic_key, samples_path(folder_name))
    tcp_dict = load_results(tcp_key, samples_path(folder_name))

    quic_stats = apply_func_to_values(quic_dict, statistic_func, round_by)
    tcp_stats = apply_func_to_values(tcp_dict, statistic_func, round_by)

    return quic_stats, tcp_stats


def plot_graphs(samples):
    category_names = ['Handshake', 'Time to first byte', 'Content Transfer', 'Close socket']
    quic_key = 'QUIC'
    tcp_key = 'TCP/TLS'
    multiple_graphs = True if len(samples) > 1 else False
    title = ""
    results = {}

    for sample in samples:
        value = get_dataset_delay(sample)
        if not value:
            continue
        delay = f"Delay {value}"
        title = delay
        quic_results, tcp_results = get_avg_values(sample)
        results.update({f"{quic_key}-{delay}": quic_results})
        results.update({f"{tcp_key}-{delay}": tcp_results})

    survey(results, category_names, multiple_graphs=multiple_graphs)
    title = "" if multiple_graphs else title
    return title


def get_dataset_delay(folder):
    pattern = r'delay(.*)$'
    match = re.findall(pattern, folder)
    if len(match) > 0:
        return match.pop()
    return None


def plot_single_graph():
    quic_folder_name = "2021-03-08 08-21-15.964770"
    tcp_folder_name = "2021-03-08 08-53-34.612692"
    samples = "samples_threshold5_dev2_delay0"
    quic_key = "quic"
    tcp_key = "tcp"

    handshake_key = "handshakeDuration"
    byte_key = "secure-to-data"
    transfer_key = "data-to-streamEnd"
    socket_key = "streamEnd-to-socketClose"

    quic_dict = load_results(quic_key, samples_path(samples))
    tcp_dict = load_results(tcp_key, samples_path(samples))

    quic_handshake = quic_dict[handshake_key][quic_folder_name]
    quic_byte = quic_dict['server'][byte_key][quic_folder_name]
    quic_transfer = quic_dict['server'][transfer_key][quic_folder_name]
    quic_socket = quic_dict['server'][socket_key][quic_folder_name]

    tcp_handshake = tcp_dict[handshake_key][tcp_folder_name]
    tcp_byte = tcp_dict['server'][byte_key][tcp_folder_name]
    tcp_transfer = tcp_dict['server'][transfer_key][tcp_folder_name]
    tcp_socket = tcp_dict['server'][socket_key][tcp_folder_name]

    category_names = ['Handshake', 'Time to first byte', 'Content Transfer', 'Close socket']
    read_results= {
        'QUIC (Delay 0)': list(map(convert_to_ms, [quic_handshake, quic_byte, quic_transfer, quic_socket])),
        'TCP/TLS (Delay 0)': list(map(convert_to_ms, [tcp_handshake, tcp_byte, tcp_transfer, tcp_socket]))
    }

    survey(read_results, category_names)


def get_stats():
    sdev = stat.stdev
    f = stat.mean
    print("stats")
    quic_dict, tcp_dict = None, None
    values = get_value_stats("samples_threshold55_dev2_delay50", statistic_func=sdev)
    if values:
        quic_dict, tcp_dict = values
        print("quic")
        print(quic_dict)
        print("tcp")
        print(tcp_dict)


if __name__ == '__main__':
    samples = [
        "samples_threshold5_dev2_delay0",
        # "samples_threshold15_dev2_delay10",
        # "samples_threshold25_dev2_delay20",
        # "samples_threshold55_dev2_delay50"
    ]

    title = plot_graphs(samples)
    plt.yticks([])
    plt.subplots_adjust(wspace=0.15)
    plt.suptitle(title)
    plt.show()