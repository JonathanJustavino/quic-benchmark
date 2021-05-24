import os
import csv
from pathlib import Path
from statistics import mean


timestamp_file = "mod_timestamps.csv"
results = {}


def add_timestamp_to_results(result, label):
    if "QUIC" in label :
        results.update({f"{label}": [result, 0]})
    else: 
        results.update({f"{label}": [0, result]})


def convert_s_to_ms(avg_duration):
    return avg_duration * 1000


def get_avg_duration(timestamps):
    durations = []
    for sample in timestamps:
        durations.append(float(sample[-1]))
    return mean(durations)


def data_loader(path):
    folders = sorted(path.glob('*'))
    csvs = []
    for folder in folders:
        with open(f"{folder}/{timestamp_file}", "r") as file:
            reader = csv.reader(file, delimiter=",")
            for timestamps in reader:
                csvs.append(timestamps)
    return csvs


def get_path(samples_folder, socket_type):
    base_path, _ = os.path.split(os.getcwd())
    path_name = os.path.join(base_path, samples_folder, socket_type, "remote/")
    path = Path(path_name)
    return path

def gather_tcp_quic_timestamps(samples_folder, delay):
    quic_path = get_path(samples_folder, "quic")
    tcp_path = get_path(samples_folder, "tcp")
    quic_timestamps = data_loader(quic_path)
    tcp_timestamps = data_loader(tcp_path)
    quic_avg_duration = get_avg_duration(quic_timestamps)
    tcp_avg_duration = get_avg_duration(tcp_timestamps)
    format_quic = "{:.2f}".format(convert_s_to_ms(quic_avg_duration))
    format_tcp = "{:.2f}".format(convert_s_to_ms(tcp_avg_duration))
    add_timestamp_to_results(float(format_quic), f"QUIC {delay}")
    add_timestamp_to_results(float(format_tcp), f"TCP+TLS {delay}")


def get_avg_timestamp_duration():
    samples_folder = "samples/samples_threshold5_dev2_delay0"
    gather_tcp_quic_timestamps(samples_folder, "Delay 0")
    samples_folder = "samples/samples_threshold15_dev2_delay10"
    gather_tcp_quic_timestamps(samples_folder, "Delay 10")
    samples_folder = "samples/samples_threshold25_dev2_delay20"
    gather_tcp_quic_timestamps(samples_folder, "Delay 20")
    samples_folder = "samples/samples_threshold55_dev2_delay50"
    gather_tcp_quic_timestamps(samples_folder, "Delay 50")
    return results