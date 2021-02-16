import os
import shutil
from colored import fg, stylize
import asyncio
import subprocess
from utils.parser import dockerParser
from benchmarks import local_benchmark, remote_benchmark, quic_benchmark, tcp_benchmark, dump_results, docker_ping


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


async def compose_up():
    subprocess.run("docker-compose up -d", shell=True)
    

async def compose_down():
    subprocess.run("docker-compose down", shell=True)


def log_arguments(arguments):
    if arguments.__dict__['ipaddress'] == '':
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

    if not arguments.ipaddress and not arguments.server:
        local_benchmark(*benchmark)
    else:
        if arguments.server:
            remote_benchmark(benchmark[0])
        elif arguments.client:
            docker_ping(benchmark[1], arguments.ipaddress, check=True)
            remote_benchmark(benchmark[0], arguments.ipaddress, is_client=True)


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
    
    log_arguments(arguments)
    print("Docker Compose", stylize("Up", fg("yellow")))
    await compose_up()
    print("Container Setup", stylize("Finished", fg("green")))
    run_benchmark(arguments)
    print("Docker Compose", stylize("Down", fg("yellow")))
    await compose_down()


# Python 3.7+
asyncio.run(main())