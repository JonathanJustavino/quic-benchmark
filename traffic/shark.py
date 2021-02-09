import subprocess


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
    subprocess.run(command, shell=True, check=True)


@create_output_file
def capture_packets_continuously(interface, filter="", output_file="", amount_of_packets=10):
    command = f"sudo tshark -i {interface} -w {output_file} -f '{filter}' -a 'packets: {amount_of_packets}'"
    subprocess.run(command, shell=True, check=True)


def monitor_network(socket_type, interface, continuously=False):
    pkt_filter = ''

    if socket_type == 'quic':
        pkt_filter = 'udp port 1234'
    elif socket_type == 'tcp-tls':
        pkt_filter = 'tcp port 1337'

    if continuously:
        capture_packets_continuously(interface, filter=pkt_filter, output_file=f"{socket_type}")
    else:
        capture_packets(interface, filter=pkt_filter, output_file=f"{socket_type}")