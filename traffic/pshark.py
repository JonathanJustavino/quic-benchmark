import pyshark


interface = ''
interface_lo = 'lo'
interface_docker = 'br-bbd147c17183'
filter = ''
filter_tcp = 'tcp port 1337'
filter_udp = 'udp port 1234'

port_type = "tcp"

temp_flag = False
tcp_filter = True

if temp_flag:
    interface = interface_docker
else: 
    interface = interface_lo

if tcp_filter:
    filter = filter_tcp
else:
    filter = filter_udp


def capture_packets(interface, filter=""):
    capture_file = f"./traffic/{port_type}.cap"
    print("capturing packets..")
    capture = pyshark.LiveCapture(interface=interface, bpf_filter=filter, output_file=capture_file)
    #capture = pyshark.LiveCapture(interface=interface, output_file=capture_file)
    #capture.sniff(timeout=20)
    #print(capture)

    for packet in capture.sniff_continuously(packet_count=9):
        print(f"p: {packet.highest_layer}")


def gather_info():
    pass