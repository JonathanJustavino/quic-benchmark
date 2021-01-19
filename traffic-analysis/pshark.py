import pyshark


interface = 'wlp61s0'
#filter = 'tcp port 1337'
#filter = 'udp port 1234'


def capture_packets(interface, filter):
    print("capturing packets..")
    capture = pyshark.LiveCapture(interface=interface, display_filter=filter)
    capture.sniff(timeout=20)
    print(capture)


def gather_info():
    pass


capture_packets(interface, filter)