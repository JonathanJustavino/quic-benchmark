import docker


docker_client = docker.from_env()
install_cmd = "npm install"
tcp_server_cmd = "npm run tcps"
tcp_client_cmd = "npm run tcpc"
quic_server_cmd = "npm run quics"
quic_client_cmd = "npm run quicc"
tcp_socket = "tcp"

quic_benchmark = ("quic", "tcp")
tcp_benchmark = ("tcp", "quic")


def local_benchmark(server_name, client_name):
    server = docker_client.containers.get(server_name)
    client = docker_client.containers.get(client_name)
    server.exec_run(install_cmd)
    client.exec_run(install_cmd)
    stream = None
    if server_name == tcp_socket:
        server.exec_run(tcp_server_cmd, detach=True)
        _, stream =  client.exec_run(tcp_client_cmd, stream=True)
    else:
        server.exec_run(quic_server_cmd, detach=True)
        _, stream =  client.exec_run(quic_client_cmd, stream=True)
    for output in stream:
        print(str(output))
        if "File is written successfully!" in str(output):
            print("shutting down...")


def remote_benchmark(container_name, server=True, client=False):
    print("needs to be implemented")
    pass

# local_benchmark("tcp", "quic", "tcp")
# local_benchmark("quic", "tcp", "quic")