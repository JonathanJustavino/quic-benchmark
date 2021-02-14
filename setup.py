import asyncio
import subprocess
from benchmarks import local_benchmark, remote_benchmark, quic_benchmark, tcp_benchmark
from parser import dockerParser


log_helper = "-----------------------------------------"


async def compose_up():
    subprocess.run("docker-compose up -d", shell=True)
    

async def compose_down():
    subprocess.run("docker-compose down", shell=True)


def run_benchmark():
    arguments = dockerParser.parse_args()
    print(arguments)
    if arguments.quic:
        benchmark = quic_benchmark
    elif arguments.tcp:
        benchmark = tcp_benchmark

    if not arguments.ipaddress and not arguments.server:
        local_benchmark(*benchmark)
    else:
        if arguments.server:
            remote_benchmark(benchmark[0] , server=True)
        elif arguments.client:
            remote_benchmark(benchmark[0], arguments.ipaddress, client=True)
    

async def main():
    print("Docker Compose Up")
    await compose_up()
    print("Container Setup Finished")
    print(log_helper)
    print("Container Output:")
    run_benchmark()
    print(log_helper)
    print("Docker Compose Down")
    await compose_down()


# Python 3.7+
asyncio.run(main())