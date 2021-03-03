import os   
import re
import json
import shutil
import datetime


_date_1 = '2021-02-18 19:49:36.334026'
_date_2 = '2021-02-18 19:45:22.384127'

folder_filter = r'(.*measurements)'
measurement_folder = "measurements"


def filter_measurements_folders(max_rtt=67, max_mdev=7):
    benchmarks = []
    path = os.getcwd()
    path = f"{path}/{measurement_folder}"
    if not os.path.isdir(path):
        print("Directory not found: {path}")
    for root, _, files in os.walk(path):
        if len(files) == 0:
            continue
        if os.path.isfile(f"{root}/ping.json"):
            ping_json = f"{root}/ping.json"
            with open(ping_json) as f:
                data = json.load(f)
                deviation = float(data['rtt_statistics']['mdev']['value'])
                rtt = float(data['rtt_statistics']['avg']['value'])
                if deviation <= float(max_mdev) and rtt <= float(max_rtt):
                    benchmarks.append(root)
    return benchmarks


def extract_measurements(dst_folder=None, max_rtt=67, max_mdev=7):
    folders = filter_measurements_folders(max_rtt=max_rtt, max_mdev=max_mdev)
    dst_folder = get_samples_folders()
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder, exist_ok=True)
    for folder in folders:
        dst_sub_path = re.sub(folder_filter, "", folder)
        path = f"{dst_folder}{dst_sub_path}"
        print(path)
        shutil.copytree(folder, path, dirs_exist_ok=True)


def get_samples_folders(samples_folder='samples'):
    folder_filter = 'quic-benchmark'
    dst_folder = os.getcwd()
    dst_folder = re.sub(folder_filter, "", dst_folder)
    return f"{dst_folder}{samples_folder}"


def convert_to_datetime():
    path = get_samples_folders()
    socket_type = 'quic'
    network = 'remote'
    quic_path = f"{path}/{socket_type}/{network}"
    date_format = "%Y-%m-%d %H:%M:%S"
    convert = lambda x: datetime.datetime.strptime(x[:19], date_format)
    return list(map(convert, os.listdir(quic_path)))


def match_benchmark_folders():
    folders = convert_to_datetime()
    f1 = folders[0]
    f2 = folders[1]
    print(f1)
    print(f2)
    print(f2 - f1)
    print(f2 > f1)
    ...