import argparse


dockerParser = argparse.ArgumentParser(description='Choose to run with socket \
type tcp-tls or quic and service type client or server')
dockerParser.add_argument('-t', '--tcp', action='store_true', help='Use tcp-tls socket')
dockerParser.add_argument('-q', '--quic', action='store_true', help='Use quic socket')
dockerParser.add_argument('-s', '--server', action='store_true', help='Run server')
dockerParser.add_argument('-c', '--client', action='store_true', help='Run client')
dockerParser.add_argument('-ip', '--ipaddress', action='store', default="", 
                    help='Define a remote ip to the machine where server is running')

pingParser = argparse.ArgumentParser(description='Run ping with or without network usage check')
dockerParser.add_argument('-c', '--check', action='store_true', help='Run ping and check if the \
    network usage is below threshold')
dockerParser.add_argument('-p', '--ping', action='store_true', help='Run ping and document output')
dockerParser.add_argument('-t', '--threshold', action='store', default="1ms", 
                    help='Define a threshold for network  usage')