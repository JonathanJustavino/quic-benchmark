import os
import json
import subprocess


threshold = 120.0
thresholds = {
    'minimal': 1,
    'moderate': 10,
    'high': 50
}


output = "ping.json"
ping_count = 4
ping_check_count = 4
criteria = "avg"
working_dir = ""
programm_path = "ping-to-json/ping_to_json.sh"
repository = "https://github.com/richardimaoka/ping-to-json.git"


def get_programm_path():
    working_dir = os.getcwd()
    return f"{working_dir}/traffic/{programm_path}"


def check_network_usage(ip):
    command = f"touch traffic/check-{output}"
    subprocess.run(command, shell=True, check=True)
    full_path = get_programm_path()
    command = f"ping {ip} -c {ping_check_count} | {full_path} > traffic/check-{output}"
    subprocess.run(command, shell=True, check=True)

    with open(f"traffic/check-{output}", "r") as result:
        data = json.load(result)

    if float(data["rtt_statistics"][criteria]["value"]) > threshold:
        print("ping is too high")
        return False
    else:
        print("network usage is adequate")
        return True


def ping_service(ip):
    command = f"touch traffic/{output}"
    subprocess.run(command, shell=True, check=True)
    full_path = get_programm_path()
    command = f"ping {ip} -c {ping_count} | {full_path} > traffic/{output}"
    subprocess.run(command, shell=True, check=True)


def clone_ping_to_json():
    if os.path.isfile(get_programm_path()):
        return
    else:
        command = f"git clone {repository} {os.getcwd()}/traffic/ping-to-json"
        subprocess.run(command, shell=True, check=True)

