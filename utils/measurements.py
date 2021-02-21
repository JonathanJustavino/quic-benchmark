import os   
import re
import json
import shutil
import datetime


date_1 = '2021-02-18 19:49:36.334026'
date_2 = '2021-02-18 19:45:22.384127'

folder_filter = r'(.*measurements)'
measurement_folder = "measurements"



def filter_measurements_folders(threshold=7):
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
                if deviation <= threshold:
                    benchmarks.append(root)
    return benchmarks


def extract_measurements(dst_folder=None, threshold=7):
    folders = filter_measurements_folders(threshold=threshold)
    dst_folder = "/Users/jonathanl./Documents/Studium/Master/Semester05/KP-RN/samples"
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder, exist_ok=True)
    for folder in folders:
        dst_sub_path = re.sub(folder_filter, "", folder)
        path = f"{dst_folder}{dst_sub_path}"
        print(path)
        shutil.copytree(folder, path, dirs_exist_ok=True)


def match_benchmark_folders():
    ...