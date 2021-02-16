import os
import asyncio
import subprocess
from utils.parser import dockerParser
from benchmarks import local_benchmark, remote_benchmark, quic_benchmark, tcp_benchmark, dump_results, docker_ping


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
    

async def main():
    arguments = dockerParser.parse_args()
    log_arguments(arguments)
    print("Docker Compose Up")
    await compose_up()
    print("Container Setup Finished")
    run_benchmark(arguments)
    print("Docker Compose Down")
    await compose_down()


# Python 3.7+
asyncio.run(main())