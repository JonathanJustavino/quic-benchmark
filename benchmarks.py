import docker


docker_client = docker.from_env()
install_cmd = "npm install"
tcp_server_cmd = "npm run tcps"
tcp_client_cmd = "npm run tcpc"
quic_server_cmd = "npm run quics"
quic_client_cmd = "npm run quicc"
tcp_socket = "tcp"


def local_benchmark(server_name, client_name, socket_type):
    server = docker_client.containers.get(server_name)
    client = docker_client.containers.get(client_name)
    server.exec_run(install_cmd)
    client.exec_run(install_cmd)
    if socket_type == tcp_socket:
        server.exec_run(tcp_server_cmd)
        client.exec_run(tcp_client_cmd)
        return
    server.exec_run(quic_server_cmd)
    client.exec_run(quic_client_cmd)

    print(client.logs())
    print(server.logs())


def remote_benchmark(container_name, server=True, client=False):
    print("needs to be implemented")
    pass
