import os
import json
import subprocess
from parser import pingParser


thresholds = {
    'minimal': 1,
    'moderate': 10,
    'high': 50
}


output = "./utils/ping.json"
output_check = "./utils/check-ping.json"
ping_count = 4
ping_check_count = 4
criteria = "avg"
working_dir = ""
programm_path = "../ping-to-json/ping_to_json.sh"


def check_network_usage(ip):
    command = f"touch {output_check}"
    subprocess.run(command, shell=True, check=True)
    command = f"ping {ip} -c {ping_check_count} | {programm_path} > {output_check}"
    subprocess.run(command, shell=True, check=True)

    with open(f"{output_check}", "r") as result:
        data = json.load(result)

    if float(data["rtt_statistics"][criteria]["value"]) > threshold:
        print("ping is too high")
        return False
    else:
        print("network usage is adequate")
        return True


def ping_service(ip):
    command = f"touch {output}"
    subprocess.run(command, shell=True, check=True)
    command = f"ping {ip} -c {ping_count} | {programm_path} > {output}"
    subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    arguments = pingParser.parse_args()
    threshold = float(arguments.threshold)
    if arguments.check:
        print("checking network usage...")
        check_network_usage(arguments.ipaddress)
    else:
        print("ping service...")
        ping_service(arguments.ipaddress)