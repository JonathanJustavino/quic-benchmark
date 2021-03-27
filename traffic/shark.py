import subprocess
import docker


network = "quic-benchmark_default"


def create_output_file(func):
    def inner(*args, **kwargs):
        out_file = kwargs.get('output_file')
        command = f"sudo touch ./traffic/{out_file}.pcap"
        subprocess.run(command, shell=True, check=True)
        func(*args, **kwargs)
    return inner


@create_output_file
def capture_packets(interface, filter="", output_file="", time=20):
    command = f"sudo tshark -i {interface} -w './traffic/{output_file}.pcap' -f '{filter}' -a 'duration: {time}'"
    output = subprocess.run(command, shell=True, check=True, capture_output=True)
    output = output.stderr.decode('utf-8').split("\n")
    for line in output:
        if "packets captured" in line:
            print(f"Tshark: {line}")


def get_network_interface():
    client = docker.from_env()
    nets = client.networks.get(network)
    interface = f"br-{nets.attrs['Id'][:12]}"
    return interface


def monitor_network(socket_type):
    pkt_filter = ''
    # interface = get_network_interface()
    interface = "wlp61s0"

    if socket_type == 'quic':
        pkt_filter = 'udp port 443'
    elif socket_type == 'tcp':
        pkt_filter = 'tcp port 443'

    capture_packets(interface, filter=pkt_filter, output_file=f"{socket_type}")