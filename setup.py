import os
import time
import shutil
import asyncio
import subprocess
from threading import Thread
from colored import fg, stylize
from traffic.delay import add_delay
from utils.parser import dockerParser
from traffic.shark import monitor_network
from utils.measurements import extract_measurements, match_benchmark_folders
from benchmarks.benchmarks import local_benchmark, remote_benchmark, quic_benchmark, tcp_benchmark, dump_results, docker_ping, get_measurement_path, move_results


network = ("local", "remote")
socket_type = ("quic", "tcp")
measurements_folder = "measurements"


def log_helper(func):
    def wrapper(*args, **kwargs):
        _, columns = os.popen('stty size', 'r').read().split()
        count = int(columns)
        print("-" * count)
        print("Container Output:")
        func(*args, **kwargs)
        print("-" * count)
    return wrapper


def start_thread(*args, **kwargs):
    if 'target' not in kwargs.keys():
        print("No target function set")
        return
    parameter = list(kwargs.values())
    target = kwargs['target']
    del kwargs['target']
    thread = Thread(target=target, kwargs=kwargs)

    thread.start()
    return thread


async def compose_up():
    subprocess.run("docker-compose up -d", shell=True)
    

async def compose_down():
    subprocess.run("docker-compose down", shell=True)


def log_arguments(arguments):
    if arguments.__dict__['ipaddress'] == '' and not arguments.server:
        print("Local")
    else:
        print("Remote")
    for arg in arguments.__dict__:
        if arg == "ipaddress" and arguments.__dict__[arg]:
            print(f"Remote address: {arguments.__dict__[arg]}")
            continue
        if arguments.__dict__[arg]:
            print(arg.capitalize())


@log_helper
def run_benchmark(arguments):
    if arguments.quic:
        benchmark = quic_benchmark
    elif arguments.tcp:
        benchmark = tcp_benchmark
    socket_type = benchmark[0]

    if not arguments.ipaddress and not arguments.server:
        path = get_measurement_path(socket_type, network[0])
        local_benchmark(*benchmark, results_path=path)
    else:
        if arguments.server:
            path = get_measurement_path(socket_type, network[1])
            remote_benchmark(benchmark[0], results_path=path)
            return
        if arguments.client:
            delay = float(arguments.delay)
            add_delay(benchmark[1], delay)
            threshold = float(arguments.threshold) + delay
            # Warmup ping
            docker_ping(benchmark[1], arguments.ipaddress, threshold=threshold, check=True)
            low_network_usage = docker_ping(benchmark[1], arguments.ipaddress, threshold=threshold, check=True)
            if not low_network_usage:
                return
            path = get_measurement_path(socket_type, network[1])
            ping_thread = start_thread(target=docker_ping, container=benchmark[1], ip=arguments.ipaddress, threshold=threshold)
            shark_thread = start_thread(target=monitor_network, socket_type=socket_type)
            time.sleep(3)
            remote_benchmark(benchmark[0], arguments.ipaddress, is_client=True, results_path=path)
            ping_thread.join()
            shark_thread.join()
            move_results(path, socket_type, threshold=threshold, delay=delay)


def create_measurements():
    if not os.path.isdir(measurements_folder):
        for s_type in socket_type:
            for net_type in network:
                os.makedirs(f"{measurements_folder}/{s_type}/{net_type}", exist_ok=True)


def clean_measurements():
    print("Removing measurements")
    path = f"{os.getcwd()}/measurements"
    if os.path.isdir(path):
        shutil.rmtree(path)
    exit()


async def main():
    arguments = dockerParser.parse_args()
    if not os.path.isdir(measurements_folder):
        create_measurements()
    if arguments.clean:
        clean_measurements()

    if arguments.extract:
        # print("Extracting")
        # extract_measurements(threshold=7)
        match_benchmark_folders()
        exit()
    
    log_arguments(arguments)
    print("Docker Compose", stylize("Up...", fg("yellow")))
    await compose_up()
    print("Container Setup", stylize("Finished", fg("green")))
    run_benchmark(arguments)
    print("Docker Compose", stylize("Down...", fg("yellow")))
    await compose_down()


# Python 3.7+
asyncio.run(main())