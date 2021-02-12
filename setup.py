import asyncio
import subprocess
from benchmarks import local_benchmark


container_1 = "qnode"
container_2 = "qnode2"
tcp_socket = "tcp"
quic_socket = "quic"


async def compose_up():
    subprocess.run("docker-compose up -d", shell=True)
    

async def compose_down():
    subprocess.run("docker-compose down", shell=True)


async def main():
    print("compose up")
    await compose_up()
    print("container setup finished")
    local_benchmark(container_1, container_2, tcp_socket)
    await compose_down()


# Python 3.7+
asyncio.run(main())