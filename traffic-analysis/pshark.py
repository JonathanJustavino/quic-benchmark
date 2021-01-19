import pyshark


interface = 'wlp61s0'
#filter = 'tcp port 1337'
#filter = 'udp port 1234'
# bpf_filter=filter
port_type = "tcp"

def capture_packets(interface, filter):
    capture_file = f"{port_type}.cap"
    print("capturing packets..")
    capture = pyshark.LiveCapture(interface=interface, output_file=capture_file)
    capture.sniff(timeout=20)
    print(capture)


def gather_info():
    pass


capture_packets(interface, filter)