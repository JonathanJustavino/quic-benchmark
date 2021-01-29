import docker
import sys
import subprocess
import tarfile
import json
import argparse
from threading import Thread
from io import BytesIO
from pythonping import ping
from traffic.shark import monitor_network


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
    container = client.containers.create("ws2018sacc/experimentalnodejs:15.6", 
        command=command, 
        name = name, 
        ports=port, 
        detach=True)
    return container


def start_container(network, socket_type, container_type, port, ip):
    container_name = get_container_name(socket_type, container_type)
    start_cmd = f"node scripts/{container_name}.js"
    try:
        container = create_container(start_cmd, container_name, port)
    except: 
        print(f"An error occured, deleting containers:\n{container_name}")
        remove_container(container_name)
        return
    network.connect(container, ipv4_address=ip)
    container.start()
    container.wait()
    pull_measurements(container_name, f"{socket_type}-benchmark-{container_type}.json")


def remove_container(container_name):
    if not args.debug:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()


def get_container_name(socket_type, container_type):
    return f"{socket_type}-{container_type}"


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


def get_network_interface():
    nets = client.networks.get("nodejs_net")
    return nets.attrs['Id']


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Choose to run with socket \
    type tcp-tls or quic and service type client or server')
    parser.add_argument('-t', '--tcp', action='store_true', help='Use tcp-tls socket')
    parser.add_argument('-q', '--quic', action='store_true', help='Use quic socket')
    parser.add_argument('-d', '--debug', action='store_true', default=False,  
                        help='Do not remove container for inspect purposes')
    parser.add_argument('-s', '--server', action='store_true', help='Run server')
    parser.add_argument('-c', '--client', action='store_true', help='Run client')
    parser.add_argument('-ip', '--ipaddress', action='store_const', 
                        const="", default="", 
                        help='Define a remote ip to the machine where server is running')

    parser.print_help()
    args = parser.parse_args()

    port = ""
    if args.server:
        container_type = "server"
    if args.client:
        container_type = "client"

    public_ip = args.ipaddress

    interface = "br-bbd147c17183"
    interface = get_network_interface()

    if args.quic:
        socket_type = "quic"
        cap_filter = "udp port 1234"
        if args.server:
            ip = "192.168.52.38"
            port = 1234
        elif args.client:
            ip = "192.168.52.39"
    elif args.tcp:
        socket_type = "tcp-tls"
        cap_filter = "tcp port 1337"
        if args.server:
            port = 1337
            ip = "192.168.52.36"
        elif args.client:
            ip = "192.168.52.37"


    build_image()
    network = create_network()
    container_thread = None
    start_thread(target=start_container, network=network, socket_type=socket_type, container_type=container_type, port=port, ip=ip)
    if args.client:
        start_thread(target=monitor_network, socket_type=socket_type, continuously=False)
    start_thread(target=ping_container, public_ip=public_ip)