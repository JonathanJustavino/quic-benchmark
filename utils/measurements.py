import os   
import re
import json
import shutil
import datetime


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
    dst_folder = get_folder_path()
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder, exist_ok=True)
    for folder in folders:
        dst_sub_path = re.sub(folder_filter, "", folder)
        path = f"{dst_folder}{dst_sub_path}"
        print(path)
        shutil.copytree(folder, path, dirs_exist_ok=True)


def get_folder_path(samples_folder='samples'):
    folder_filter = 'quic-benchmark'
    dst_folder = os.getcwd()
    dst_folder = re.sub(folder_filter, "", dst_folder)
    return f"{dst_folder}{samples_folder}"


def filter_sole_folders(socket_type):
    server_files = (f"{socket_type}-benchmark-server.json", "ssl-keys.log")
    client_files = (f"{socket_type}-benchmark-client.json", f"{socket_type}.pcap", "ping.json")
    server_list = []
    client_list = []
    deletables = []
    path = get_folder_path()
    path = f"{path}/{socket_type}/remote"
    folders = os.listdir(path)
    osx_file = ".DS_Store"
    if osx_file in folders:
        folders.remove(osx_file)
    for folder in folders:
        files = os.listdir(f"{path}/{folder}")
        client = is_client(files, client_files)
        server = is_server(files, server_files)
        if not server and not client:
            deletables.append(string_to_datetime(folder))
            continue
        if server:
            server_list.append(folder)
        if client:
            client_list.append(folder)
        if server and client:
            print("Samples have been merged previously, aborting...")
            exit()
    server_list.sort()
    client_list.sort()
    return server_list, client_list, deletables


def string_to_datetime(folder):
    formatter = "%Y-%m-%d %H-%M-%S.%f"
    return datetime.datetime.strptime(folder, formatter)


def datetime_to_string(date):
    formatter = "%Y-%m-%d %H-%M-%S.%f"
    return datetime.datetime.strftime(date, formatter)


def remove_folders(folders, path):
    for date in folders:
        folder = datetime_to_string(date)
        shutil.rmtree(f"{path}{folder}", ignore_errors=True)


def match_folders(socket_type):
    server_list, client_list, deletables = filter_sole_folders(socket_type)
    if not server_list or not client_list:
        return [], deletables
    server_list = list(map(string_to_datetime, server_list))
    client_list = list(map(string_to_datetime, client_list))
    sample_pairs = []
    matches = []
    len_server = len(server_list)
    for i in range(len_server):
        server_date = server_list[i]
        if i < len_server - 1:
            next_server_date = server_list[i + 1]
            matches.append(server_date)
            for date in client_list:
                if date > server_date and date < next_server_date:
                    matches.append(date)
                    client_list.remove(date)
        if len(matches) < 2:
            if matches:
                deletables.append(matches[0])
            matches = []
            continue
        sample_pairs.append((matches[0], matches[len(matches) - 1]))
        matches = []

    last_server = server_list[len_server - 1]
    last_client = client_list[len(client_list) - 1]
    if last_client > last_server:
        sample_pairs.append((last_server, last_client))
        client_list.remove(last_client)
    deletables += client_list
    return sample_pairs, deletables


def merge_folder():
    quic_pairs, quic_deletables = match_folders('quic')
    quic_path = f"{get_folder_path()}/quic/remote/"
    tcp_pairs, tcp_deletables = match_folders('tcp')
    tcp_path = f"{get_folder_path()}/tcp/remote/"

    remove_folders(tcp_deletables, tcp_path)
    remove_folders(quic_deletables, quic_path)

    if quic_pairs:
        print("Merging QUIC")
        f = lambda tup: (f"{quic_path}{datetime_to_string(tup[0])}", f"{quic_path}{datetime_to_string(tup[1])}")
        quic_pairs = list(map(f, quic_pairs))
        merge_pairs(quic_pairs)
    if tcp_pairs:
        print("Merging TCP")
        f = lambda tup: (f"{tcp_path}{datetime_to_string(tup[0])}", f"{tcp_path}{datetime_to_string(tup[1])}")
        tcp_pairs = list(map(f, tcp_pairs))
        merge_pairs(tcp_pairs)
    return


def merge_pairs(pairs):
    for pair in pairs:
        shutil.copytree(pair[1], pair[0], dirs_exist_ok=True)
        shutil.rmtree(pair[1])    


def is_client(files, client_list):
    for client_file in client_list:
        if client_file not in files:
            return False
    return True


def is_server(files, server_list):
    for server_file in server_list:
        if server_file not in files:
            return False
    return True
