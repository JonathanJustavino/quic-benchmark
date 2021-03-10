from visualize_events.plot_timeplan import *
from visualize_events.dataloader import load_results


def get_samples_path(samples_folder='samples'):
    folder_filter = 'quic-benchmark'
    dst_folder = os.getcwd()
    dst_folder = re.sub(folder_filter, samples_folder, dst_folder)
    return f"{dst_folder}"


quic_key = "quic"
tcp_key = "tcp"

quic_dict = load_results(quic_key, get_samples_path())
tcp_dict = load_results(tcp_key, get_samples_path())

session_key = "ready-to-session"
handshake_key = "handshakeDuration"
byte_key = "secure-to-data"
transfer_key = "data-to-streamEnd"
socket_key = "streamEnd-to-socketClose"

quic_session = quic_dict[session_key]
quic_handshake = quic_dict[handshake_key]
quic_byte = quic_dict['server'][byte_key]
quic_transfer = quic_dict['server'][transfer_key]
quic_socket = quic_dict['server'][socket_key]

tcp_session = tcp_dict[session_key]
tcp_handshake = tcp_dict[handshake_key]
tcp_byte = tcp_dict['server'][byte_key]
tcp_transfer = tcp_dict['server'][transfer_key]
tcp_socket = tcp_dict['server'][socket_key]

category_names = ['Create session', 'Handshake', 'Time to first byte',
                  'Content Transfer', 'Close socket']

convert_to_ms = lambda t: t / 1000

results = {
    'QUIC': list(map(convert_to_ms, [quic_session, quic_handshake, quic_byte, quic_transfer, quic_socket])),
    'TCP/TLS': list(map(convert_to_ms, [tcp_session, tcp_handshake, tcp_byte, tcp_transfer, tcp_socket]))
}

print(results)

survey(results, category_names)
plt.xlabel("Milliseconds")
plt.ylabel("Socket type")
plt.show()