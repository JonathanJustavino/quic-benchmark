import os
import json
from statistics import median, stdev
from dateutil import parser, relativedelta


def load_folders(socket_type, path):
    path = f"{path}/{socket_type}/remote/"
    folders = os.listdir(path)

    osx_file = ".DS_Store"
    if osx_file in folders:
        folders.remove(osx_file)

    folders.sort()
    return folders


def read_results(path, folders, socket_type, results):
    server = f"{socket_type}-benchmark-server.json"
    client = f"{socket_type}-benchmark-client.json"
    for folder in folders:
        client_path = f"{path}/{socket_type}/remote/{folder}/{client}"
        server_path = f"{path}/{socket_type}/remote/{folder}/{server}"
        accumulate_client_data(client_path, results, folder)
        accumulate_server_data(server_path, results, folder)


def load_ping(path, socket_type, folders, results):
    rtt_stats = "rtt_statistics"
    stats = ["min", "max", "mdev"]
    setup_ping_properties(results, rtt_stats, stats)
    for folder in folders:
        file = f"{path}/{socket_type}/remote/{folder}/ping.json"
        with open(file, 'r') as f:
            ping = json.load(f)
            results['ping'][rtt_stats][stats[0]] += float(ping[rtt_stats][stats[0]]['value'])
            results['ping'][rtt_stats][stats[1]] += float(ping[rtt_stats][stats[1]]['value'])
            results['ping'][rtt_stats][stats[2]] += float(ping[rtt_stats][stats[2]]['value'])


def setup_ping_properties(results, parent_key, keys):
    if parent_key not in results['ping']:
        results['ping'][parent_key] = {}
    for key in keys:
        results['ping'][parent_key][key] = 0.0


def accumulate_data(data, results, folder, side='server'):
    for key_1, value_1 in data:
        for key_2, value_2 in data:
            if key_1 is key_2 or not value_1 or not value_2:
                continue
            date_1 = parser.parse(value_1)
            date_2 = parser.parse(value_2)
            if date_1 < date_2:
                new_key = f"{key_1}-to-{key_2}"
                if new_key not in results[side]:
                    results[side][f"{key_1}-to-{key_2}"] = {folder: 0}
                results[side][f"{key_1}-to-{key_2}"][folder] = relativedelta.relativedelta(date_2, date_1).microseconds
    

def accumulate_client_data(file, results, folder):
    with open(file, 'r') as f:
        data = json.load(f).items()
        accumulate_data(data, results, folder, side='client')


def accumulate_server_data(file, results, folder):
    duration = 'handshakeDuration'
    with open(file, 'r') as f:
        data = json.load(f)
        events = data["events"].items()
        accumulate_data(events, results, folder)
        if duration not in results:
            results[duration] = {folder: 0}
        results[duration][folder] = float(data["durations"]["handshakeDurationInNs"]) / 1000


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


def average_results(results):
    for key, _ in results['server'].items():
        values = results['server'][key].values()
        results['server'][key]['avg'] = sum(values) / len(values)
    for key, _ in results['client'].items():
        values = results['client'][key].values()
        results['client'][key]['avg'] = sum(values) / len(values)
    values = results['handshakeDuration'].values()
    results['handshakeDuration']['avg'] = sum(values) / len(values)


def median_results(results):
    for key, _ in results['server'].items():
        values = results['server'][key].values()
        results['server'][key]['median'] = median(values)
    for key, _ in results['client'].items():
        values = results['client'][key].values()
        results['client'][key]['median'] = median(values)
    values = results['handshakeDuration'].values()
    results['handshakeDuration']['median'] = median(values)


def stdev_results(results):
    for key, _ in results['server'].items():
        values = results['server'][key].values()
        results['server'][key]['stdev'] = stdev(values)
    for key, _ in results['client'].items():
        values = results['client'][key].values()
        results['client'][key]['stdev'] = stdev(values)
    values = results['handshakeDuration'].values()
    results['handshakeDuration']['stdev'] = stdev(values)


def load_results(socket_type, path):
    results = {'server': {}, 'client': {}}
    folders = load_folders(socket_type, path)
    read_results(path, folders, socket_type, results)
    average_results(results)
    median_results(results)
    stdev_results(results)
    return results


def load_ping_results(socket_type, path):
    results = {'ping': {}}
    folders = load_folders(socket_type, path)
    load_ping(path, socket_type, folders, results)
    return results