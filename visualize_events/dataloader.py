# from ..utils.measurements import get_folder_path
import os
import json
from dateutil import parser, relativedelta


def load_folders(socket_type, path):
    path = f"{path}/{socket_type}/remote/"
    folders = os.listdir(path)

    osx_file = ".DS_Store"
    if osx_file in folders:
        folders.remove(osx_file)

    add_path = lambda f: f"{path}{f}"
    folders = list(map(add_path, folders))
    return folders


def read_results(folders, socket_type, results):
    server = f"{socket_type}-benchmark-server.json"
    client = f"{socket_type}-benchmark-client.json"
    for folder in folders:
        client_path = f"{folder}/{client}"
        server_path = f"{folder}/{server}"
        accumulate_client_data(client_path, results)
        accumulate_server_data(server_path, results)
        accumulate_ready_to_session(client_path, server_path, results)


def accumulate_data(data, results, side='server'):
    for key_1, value_1 in data:
        for key_2, value_2 in data:
            if key_1 is key_2 or not value_1 or not value_2:
                continue
            date_1 = parser.parse(value_1)
            date_2 = parser.parse(value_2)
            if date_1 < date_2:
                new_key = f"{key_1}-to-{key_2}"
                if new_key in results[side]:
                    results[side][f"{key_1}-to-{key_2}"] += relativedelta.relativedelta(date_2, date_1).microseconds
                    continue
                results[side][f"{key_1}-to-{key_2}"] = relativedelta.relativedelta(date_2, date_1).microseconds
    

def accumulate_client_data(file, results):
    with open(file, 'r') as f:
        data = json.load(f).items()
        accumulate_data(data, results, side='client')


def accumulate_server_data(file, results):
    duration = 'handshakeDuration'
    with open(file, 'r') as f:
        data = json.load(f)
        events = data["events"].items()
        accumulate_data(events, results)
        if duration not in results:
            results[duration] = float(data["durations"]["handshakeDurationInNs"]) / 1000
            return
        results[duration] += float(data["durations"]["handshakeDurationInNs"]) / 1000


def accumulate_ready_to_session(client_path, server_path, results):
    rdy_2_session = 'ready-to-session'
    with open(client_path, 'r') as c, open(server_path, 'r') as s:
        client_data = json.load(c)
        server_data = json.load(s)
        client_date = parser.parse(client_data['ready'])
        server_date = parser.parse(server_data['events']['session'])
        if rdy_2_session not in results:
            results[rdy_2_session] = relativedelta.relativedelta(server_date, client_date).microseconds
            return
        results[rdy_2_session] += relativedelta.relativedelta(server_date, client_date).microseconds


def average_results(results, count):
    for key, _ in results['server'].items():
        results['server'][key] /= count
    for key, _ in results['client'].items():
        results['client'][key] /= count
    results['handshakeDuration'] /= count
    results['ready-to-session'] /= count


def load_results(socket_type, path):
    results = {'ping': {}, 'server': {}, 'client': {}}
    folders = load_folders(socket_type, path)
    folder_count = len(folders)
    read_results(folders, socket_type, results)
    average_results(results, folder_count)
    return results