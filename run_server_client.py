import docker
import sys
import subprocess
import tarfile
import json
from threading import Thread
from io import BytesIO
from pythonping import ping
from traffic.pshark import capture_packets


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
    network = None
    try:
        network = client.networks.get("nodejs_net")
    except:
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


def start_container(network, socket_type, container_type, port, ip):
    start_cmd = f"node scripts/{socket_type}-{container_type}.js"
    con_name = f"{socket_type}-{container_type}"
    container = create_container(start_cmd, con_name, port)
    network.connect(container, ipv4_address=ip)
    container.start()
    container.wait()
    pull_measurements(con_name, f"{socket_type}-benchmark-{container_type}.json")


def remove_container(container_name):
    container = client.containers.get(container_name)
    container.stop()
    container.remove()


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
    remove_container(container_name)


def ping_container(target, count=10):
    response_list = ping(target, verbose=True, count=count)
    my_list = list(response_list._responses)
    f = lambda x: f"{x}"

    ping_response = {
        "avg rtt(ms)": response_list.rtt_avg_ms, # average round-trip time in miliseconds
        "min rtt(ms)": response_list.rtt_min_ms, # minimum round-trip time in miliseconds
        "max rtt(ms)": response_list.rtt_max_ms, # maximum round-trip time in miliseconds
        "packet loss": response_list.packet_loss, # number of packets lost
        "responses": list(map(f, my_list)) # list of pings
    }

    with open('ping.json', 'w') as fp:
        json.dump(ping_response, fp, indent=2)


def start_thread(**kwargs):
    if 'target' not in kwargs.keys():
        print("No target function set")
        return
    parameter = list(kwargs.values())
    thread = Thread(target=kwargs['target'], args=(parameter[1:]))
    thread.start()
    thread.join()


if __name__ == "__main__":
    socket_type = sys.argv[1]
    container_type = sys.argv[2]
    public_ip = ""  
    if len(sys.argv) > 3:
        public_ip = sys.argv[3]

    port = ""

    if socket_type == "quic":
        interface = "br-bbd147c17183"
        cap_filter = "udp port 1234"
        if container_type == "server":
            ip = "192.168.52.38"
            port = 1234
        elif container_type == "client":
            ip = "192.168.52.39"
    elif socket_type == "tcp-tls":
        interface = "lo"
        cap_filter = "tcp port 1337"
        if container_type == "server":
            port = 1337
            ip = "192.168.52.36"
        elif container_type == "client":
            ip = "192.168.52.37"

    build_image()
    network = create_network()

    if container_type == 'shark':
        start_thread(target=capture_packets, interface=interface, filter=cap_filter)

    start_thread(target=start_container, network=network, socket_type=socket_type, container_type=container_type, port=port, ip=ip)
    start_thread(target=ping_container, public_ip=public_ip)
