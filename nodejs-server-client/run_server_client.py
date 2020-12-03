import docker
import sys
import subprocess


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
        tcp_tls_server = client.containers.run("nodejs:experimental", command="node tcp-tls-server.js", 
        name = "tcp_tls_server", ports={'1337/tcp': 1337}, detach=True)
        tcp_tls_client = client.containers.run("nodejs:experimental", command="node tcp-tls-client.js", 
        name = "tcp_tls_client", detach=True)
        network.connect(tcp_tls_server, ipv6_address="192.168.52.36")
        network.connect(tcp_tls_client, ipv6_address="192.168.52.37")
    if socket_type == "quic":
        quic_server = client.containers.run("nodejs:experimental", command="node quic-server.js", 
        name = "quic_server", ports={'1234/udp': 1234}, detach=True)
        quic_client = client.containers.run("nodejs:experimental", command="node quic-client.js", 
        name = "quic_client", detach=True)
        network.connect(quic_server, ipv4_address="192.168.52.38")
        network.connect(quic_client, ipv4_address="192.168.52.39")


def delete_existing_containers():
    print("deleting containers")
    for con in client.containers.list():
        con.stop()
    client.containers.prune()


if __name__ == "__main__":
    socket_type = sys.argv[1]
    delete_existing_containers()
    build_image()
    network = create_network()
    run_container_and_connect_to_network(network, socket_type)
