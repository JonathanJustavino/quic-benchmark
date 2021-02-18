import docker


client = docker.from_env()


def add_delay(container_name, milliseconds=0):
    print(f"Adding network delay of {milliseconds}ms")
    container = client.containers.get(container_name)
    tc_cmd = f"tc qdisc add dev eth0 root netem delay {milliseconds}ms"
    _, stream =  container.exec_run(tc_cmd, stream=True)
    for byte_stream in stream:
        print(byte_stream.decode('utf-8'))