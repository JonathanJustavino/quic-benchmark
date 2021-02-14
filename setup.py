import asyncio
import subprocess
from benchmarks import local_benchmark, quic_benchmark, tcp_benchmark


log_helper = "-----------------------------------------"


async def compose_up():
    subprocess.run("docker-compose up -d", shell=True)
    

async def compose_down():
    subprocess.run("docker-compose down", shell=True)


async def main():
    print("Docker Compose Up")
    await compose_up()
    print("Container Setup Finished")
    print(log_helper)
    print("Container Output:")
    local_benchmark(*tcp_benchmark)
    print(log_helper)
    print("Docker Compose Down")
    await compose_down()


# Python 3.7+
asyncio.run(main())