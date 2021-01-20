import pyshark

# packet.layer.field_names: alle möglichen Attribute einer Layer zB destination adresse usw.

if __name__ == '__main__':
    cap = pyshark.FileCapture('tcp.cap')

    # pyshark.packet.packet.Packet
    packet = cap[5]

    # pyshark.packet.packet.Packet -> dict,
    # weil im "pyshark.packet.packet.Packet" nicht ganz klar ist,
    # wie die keys zu den values heißen
    vars_packet = vars(packet)

    # alle keys in packet-dict
    # print(vars_packet.keys())

    # alle Attribute in pyshark.packet.packet.Packet
    # print("Attribute in pyshark.packet.packet.Packet:", packet.__dict__)

    # Gesamte Paketlänge, die gecaptured wurde
    capt_pack_lenght = vars_packet['captured_length']
    print('Total captured packet length: ', capt_pack_lenght)

    # ----  Get different layers: ------
    # vars_packet['layers'] == [<ETH Layer>, <IP Layer>, <UDP Layer>, <DATA Layer>]

    # Ethernet layer -> kp wie das Attribut im "pyshark.packet.packet.Packet" heißt,
    # deshalb hole ich die aus dem dict
    layer_ethernet = vars_packet['layers'][0]

    # IP Layer -> steht in Doku dass man sie mit 'IP' über "pyshark.packet.packet.Packet" erreicht
    layer_ip = packet['IP']

    # UDP Layer
    layer_udp = vars_packet['layers'][2]

    # PAYLOAD / Data
    payload = vars_packet['layers'][3]
    print('payload länge: ', payload.len)

    # ---- overhead berechnen ----
    # Overhead = (gesamtpaket länge) - (payload länge)
    overhead = int(capt_pack_lenght) - int(payload.len)
    print("overhead: ", overhead)
