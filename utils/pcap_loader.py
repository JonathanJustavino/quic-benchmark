import os
import csv
from pathlib import Path
from statistics import mean


timestamp_file = "mod_timestamps.csv"


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


def get_path():
    base_path = os.getcwd()
    samples_folder = "samples/samples_threshold5_dev2_delay0"
    socket_type = "tcp"
    path_name = os.path.join(base_path, samples_folder, socket_type, "remote/")
    path = Path(path_name)
    return path


def get_avg_timestamp_duration():
    path = get_path()
    timestamps = data_loader(path)
    avg_duration = get_avg_duration(timestamps)
    return convert_s_to_ms(avg_duration)