import pyshark

# payload = packetsize - overhead
# -> overhead = packetsize - payload
# -> (Ethernet header + IPV4 header + UDP header + QUIC header) = (bytes on wire) - payload

if __name__ == '__main__':
    cap = pyshark.FileCapture('/home/amelie/Uni/RNP_Komplexpraktikum/correct_measurements/quic.pcap')

    # handshake overhead: long header packets
    
    packet = cap[1]
    layer_quic = packet['QUIC']
    # print(layer_quic)

    vars_packet = vars(packet)
    #print(vars_packet['layers'])
    print(vars_packet['layers'][3])
    print(vars_packet['layers'][4])