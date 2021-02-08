import pyshark

if __name__ == '__main__':
    cap = pyshark.FileCapture('/home/amelie/Uni/RNP_Komplexpraktikum/correct_measurements/tcp.pcap')
    packet = cap[5]
    print(packet)