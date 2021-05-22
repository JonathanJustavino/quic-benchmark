import os
import csv
from pathlib import Path
from statistics import mean


timestamp_file = "mod_timestamps.csv"
results = {}


def add_timestamp_to_results(result, socket_type):
    results.update({f"{socket_type}": [result]})


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

def gather_tcp_quic_timestamps(samples_folder):
    tcp_path = get_path(samples_folder, "tcp")
    quic_path = get_path(samples_folder, "quic")
    tcp_timestamps = data_loader(tcp_path)
    quic_timestamps = data_loader(quic_path)
    tcp_avg_duration = get_avg_duration(tcp_timestamps)
    quic_avg_duration = get_avg_duration(quic_timestamps)
    add_timestamp_to_results(convert_s_to_ms(tcp_avg_duration), "tcp")
    add_timestamp_to_results(convert_s_to_ms(quic_avg_duration), "quic")


def get_avg_timestamp_duration():
    samples_folder = "samples/samples_threshold5_dev2_delay0"
    gather_tcp_quic_timestamps(samples_folder)
    return results