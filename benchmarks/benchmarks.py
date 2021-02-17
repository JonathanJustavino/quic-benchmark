import os
import re
import shutil
import docker
import tarfile
import datetime
from io import BytesIO
from os import path as os_path


docker_client = docker.from_env()
install_cmd = "npm install"

container_commands = {
    "tcp": {
        "server_cmd": "npm run tcps",
        "client_cmd": "npm run tcpc",
    },
    "quic": {
        "server_cmd": "npm run quics",
        "client_cmd": "npm run quicc"
    }
}

tcp_socket = "tcp"

quic_benchmark = ("quic", "tcp")
tcp_benchmark = ("tcp", "quic")


def get_measurement_path(socket_type, network):
    working_dir = os.getcwd()
    date = datetime.datetime.now()
    return f"{working_dir}/measurements/{socket_type}/{network}/{date}"


def log_output(stream, supress_warnings=True):
    for byte_stream in stream:
        output = byte_stream.decode('utf-8')
        if supress_warnings:
            match = re.search("(deprecation|awk)", output)
            if match:
                continue
        print(output)
        if "File is written successfully!" in str(output):
            print("Shutting down...")


def local_benchmark(server_name, client_name, stream=None, benchmark=None, results_path=None):
    network = 'local'
    server = docker_client.containers.get(server_name)
    client = docker_client.containers.get(client_name)
    server.exec_run(install_cmd)
    client.exec_run(install_cmd)
    if server_name == tcp_socket:
        benchmark = tcp_benchmark
        server.exec_run(container_commands['tcp']['server_cmd'], detach=True)
        _, stream =  client.exec_run(container_commands['tcp']['client_cmd'], stream=True)
    else:
        benchmark = quic_benchmark
        server.exec_run(container_commands['quic']['server_cmd'], detach=True)
        _, stream =  client.exec_run(container_commands['quic']['client_cmd'], stream=True)
    log_output(stream)
    dump_results(benchmark, network, path=results_path, benchmark=benchmark)
    dump_results(benchmark, network, is_client=True, path=results_path, benchmark=benchmark)


def boot_container(container_name, command):
    print(f"\nContainer name: {container_name}\nExecuting: {command}\n")
    container = docker_client.containers.get(container_name)
    container.exec_run(install_cmd)
    _, stream =  container.exec_run(command, stream=True)
    return stream


def choose_container_type(container_cmd, is_client, benchmark, ip=''):
    if is_client:
        return boot_container(benchmark[1], f"{container_cmd['client_cmd']} {ip}")
    return boot_container(benchmark[0], container_cmd['server_cmd'])


def remote_benchmark(socket_type, ip="", is_client=False, stream=None, benchmark=None, results_path=None):
    if socket_type == tcp_socket:
        benchmark = tcp_benchmark
        stream = choose_container_type(container_commands['tcp'], is_client, tcp_benchmark, ip=ip)
    else:
        benchmark = quic_benchmark
        stream = choose_container_type(container_commands['quic'], is_client, quic_benchmark, ip=ip)
    log_output(stream)
    dump_results(benchmark, 'remote', is_client=is_client, path=results_path)


def dump_results(container_name, network, is_client=False, path=None, benchmark=None):
    socket_type = container_name[0]
    ssl_log = 'ssl-keys.log'
    container_type = "client" if is_client else "server"
    file_name = f"{socket_type}-benchmark-{container_type}.json"
    if not path:
        raise ValueError("No result path was given for dump results")
    if not os_path.exists(path):
        os.mkdir(path)
    if is_client:
        container = docker_client.containers.get(container_name[1])
    else:
        container = docker_client.containers.get(socket_type)
        extract_file(container, path, ssl_log)
    extract_file(container, path, file_name)

        
def extract_file(container, path, file_name):
    stream, _ = container.get_archive(file_name)
    file_obj = BytesIO()
    for i in stream:
        file_obj.write(i)
    file_obj.seek(0)
    tar = tarfile.open(mode='r', fileobj=file_obj)
    text = tar.extractfile(file_name)

    with open(f'{path}/{file_name}', 'wb') as file:
        for line in text:
            file.write(line)


def docker_ping(container, ip, threshold=1, check=False):
    command = f"python3 ./utils/ping.py -ip {ip} -t {threshold}"
    if check:
        command = f"{command} -c"
    container = docker_client.containers.get(container)
    _, stream = container.exec_run(command, stream=True)
    for line in stream:
        output = line.decode('utf-8')
        match = re.search("(deprecation|awk|warning)", output)
        if match:
            continue
        print(output)
        if "ping is too high" in output:
            return False
    return True


def move_results(results_path, socket_type):
    results_path = f"{results_path}/"
    shutil.move("./utils/ping.json", results_path)
    shutil.move(f"./traffic/{socket_type}.pcap", results_path)