import docker
import sys
import subprocess
import tarfile
from io import BytesIO


client = docker.from_env()


def build_image():
    print("building image")
    try: 
        client.images.get("ws2018sacc/experimentalnodejs:15.6")
    except:
        command = "docker pull ws2018sacc/experimentalnodejs:15.6"
        if sys.platform == 'linux':
            command = f"sudo {command}"
        subprocess.run(command, shell=True, check=True)


def create_network():
    print("creating network")
    network = client.networks.get("nodejs_net")
    if not network:
        ipam_pool = docker.types.IPAMPool(subnet='192.168.52.0/24', gateway='192.168.52.254')
        ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
        network = client.networks.create("nodejs_net", driver="bridge", ipam=ipam_config)
    return network


def create_container(command, name, port=None):
    if port:
        port = {f"{port}/tcp": port}
    tcp_tls_server = client.containers.create("ws2018sacc/experimentalnodejs:15.6", 
        command=command, 
        name = name, 
        ports=port, 
        detach=True)
    return tcp_tls_server


def start_container(network, socket_type, container_type):
    server = None
    client = None
    if socket_type == "tcptls":
        if container_type == "server":
            server = create_container(f"node tcp-tls-server.js {public_ip}", "tcp_tls_server", 1337)
            network.connect(server, ipv4_address="192.168.52.36")
            server.start()
        if container_type == "client":
            client = create_container(f"node tcp-tls-client.js {public_ip}", "tcp_tls_client")
            network.connect(client, ipv4_address="192.168.52.37")
            client.start()
        if server:
            server.wait()
            pull_measurements("tcp_tls_server", "tcp-benchmark-server.json")
        if client:
            client.wait()
            pull_measurements("tcp_tls_client", "tcp-benchmark-client.json")

    if socket_type == "quic":
        if container_type == "server":
            server = create_container("node quic-server.js", "quic_server", 1234)
            network.connect(server, ipv4_address="192.168.52.38")
            server.start()
        if container_type == "client":
            client = create_container(f"node quic-client.js {public_ip}", "quic_client")
            network.connect(client, ipv4_address="192.168.52.39")
            client.start()
        if server:
            server.wait()
            pull_measurements("quic_server", "quic-benchmark-server.json")
        if client:
            client.wait()
            pull_measurements("quic_client", "quic-benchmark-client.json")


def pull_measurements(container_name, file_name):
    container = client.containers.get(container_name)
    file_json = container.get_archive(file_name)
    stream, _ = file_json
    file_obj = BytesIO()
    for i in stream:
        file_obj.write(i)
    file_obj.seek(0)
    tar = tarfile.open(mode='r', fileobj=file_obj)
    text = tar.extractfile(file_name)
    with open('./{}'.format(file_name), 'wb') as file:
        for line in text:
            file.write(line)


if __name__ == "__main__":
    socket_type = sys.argv[1]
    container_type = sys.argv[2]
    public_ip = ""
    if len(sys.argv) > 3:
        public_ip = sys.argv[3]
    build_image()
    network = create_network()
    start_container(network, socket_type)
