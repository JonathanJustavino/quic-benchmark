import pyshark
from pathlib import Path
# from pcapng import FileScanner

if __name__ == '__main__':
    cap = pyshark.FileCapture('/home/amelie/Uni/RNP_Komplexpraktikum/quic-benchmark/traffic-analysis/tcp.cap')

    packet = cap[0]
    layer_ip = packet['IP']
    print(layer_ip)
    print(layer_ip.src)  # IP Adresse von 1.packet
    print(layer_ip.ttl)

    print(layer_ip.__dict__)