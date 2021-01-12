import docker
import sys
import subprocess
import tarfile
from io import BytesIO


client = docker.from_env()


def build_image():
    print("building image")
    try: 
        client.images.get("nodejs:experimental")
    except docker.errors.ImageNotFound:
        subprocess.run("sudo docker build -t nodejs:experimental .", shell=True, check=True)


def create_network():
    print("creating network")
    network = client.networks.get("nodejs_net")
    if not network:
        ipam_pool = docker.types.IPAMPool(subnet='192.168.52.0/24', gateway='192.168.52.254')
        ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
        network = client.networks.create("nodejs_net", driver="bridge", ipam=ipam_config)
    return network


def run_container_and_connect_to_network(network, socket_type):
    if socket_type == "tcptls":
        tcp_tls_server = None
        tcp_tls_client = None
        if container_type == "server" or container_type == None:
            print("creating tcp-tls-server")
            tcp_tls_server = client.containers.create("nodejs:experimental", command="node tcp-tls-server.js false", 
            name = "tcp_tls_server", ports={'1337/tcp': 1337}, detach=True)
            network.connect(tcp_tls_server, ipv4_address="192.168.52.36")
            tcp_tls_server.start()
        if container_type == "client" or container_type is None:
            print("creating tcp-tls-client")
            tcp_tls_client = client.containers.create("nodejs:experimental", command="node tcp-tls-client.js false {}".format(public_ip), 
            name = "tcp_tls_client", detach=True)
            network.connect(tcp_tls_client, ipv4_address="192.168.52.37")
            tcp_tls_client.start()
        if tcp_tls_server is not None:
            tcp_tls_server.wait()
            pull_measurements("tcp_tls_server", "tcp-benchmark-server.json")
        if tcp_tls_client is not None:
            tcp_tls_client.wait()
            pull_measurements("tcp_tls_client", "tcp-benchmark-client.json")

    if socket_type == "quic":
        quic_server = None
        quic_client = None
        if container_type == "server" or container_type == None:
            print("creating quic-server")
            quic_server = client.containers.create("nodejs:experimental", command="node quic-server.js", 
            name = "quic_server", ports={'1234/udp': 1234}, detach=True)
            network.connect(quic_server, ipv4_address="192.168.52.38")
            quic_server.start()
        if container_type == "client" or container_type == None:
            print("creating quic-client")
            quic_client = client.containers.create("nodejs:experimental", command="node quic-client.js", 
            name = "quic_client", detach=True)
            network.connect(quic_client, ipv4_address="192.168.52.39")
            quic_client.start()
        if quic_client is not None:
            quic_server.wait()
            pull_measurements("quic_server", "quic-benchmark-server.json")
        if quic_client is not None:
            quic_client.wait()
            pull_measurements("quic_client", "quic-benchmark-client.json")


def pull_measurements(container_name, file_name):
    container = client.containers.get(container_name)
    file_json = container.get_archive(file_name)
    stream, stat = file_json
    file_obj = BytesIO()
    for i in stream:
        file_obj.write(i)
    file_obj.seek(0)
    tar = tarfile.open(mode='r', fileobj=file_obj)
    text = tar.extractfile(file_name)
    file = open('./{}'.format(file_name), 'wb')
    for line in text:
        file.write(line)
    file.close()


if __name__ == "__main__":
    socket_type = sys.argv[1]
    container_type = sys.argv[2]
    if len(sys.argv) > 3:
        public_ip = sys.argv[3]
    build_image()
    network = create_network()
    run_container_and_connect_to_network(network, socket_type)
