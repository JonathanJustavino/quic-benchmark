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


def log_output(stream):
    for output in stream:
        print(str(output))
        if "File is written successfully!" in str(output):
            print("shutting down...")


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
    log_output(stream)


def boot_container(benchmark, command):
    container = docker_client.containers.get(benchmark)
    container.exec_run(install_cmd)
    _, stream =  container.exec_run(command, stream=True)
    return stream


def remote_benchmark(socket_type, ip="", server=False, client=False):
    stream = None
    if socket_type == tcp_socket:
        if client:
            client_cmd = f"{tcp_client_cmd} {ip}"
            stream = boot_container(tcp_benchmark[1], client_cmd)
        else:
            stream = boot_container(tcp_benchmark[0], tcp_server_cmd)
    else:
        if client:
            client_cmd = f"{quic_client_cmd} {ip}"
            stream = boot_container(quic_benchmark[1], client_cmd)
        else:
            stream = boot_container(quic_benchmark[0], quic_server_cmd)
    log_output(stream)