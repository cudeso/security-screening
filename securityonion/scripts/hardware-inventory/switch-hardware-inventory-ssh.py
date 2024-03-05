import paramiko
import sys
import getpass
import logging
from prettytable import PrettyTable
import requests
import shutil
import difflib
import time


def handle_client(ssh_client, username, password, command):
    '''
        Execute the command over SSH
    '''
    result = False
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logger.info("SSH to {} with {}".format(ssh_client, username))
        client.connect(ssh_client, username=username, password=password)

        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode("utf-8")

        client.close()
        stdin.close()
        result = output

    except Exception as e:
        logger.error("Error executing command on {}: {}".format(ssh_client, str(e)))

    return result


def process_client(host, output, process_type="arp"):
    '''
        Parse the output of the client
    '''
    host_output_lines = output.split("\n")
    result = []
    for line in host_output_lines:
        if process_type == "arp":
            if line.strip().startswith("Protocol"):
                continue
            elif len(line.strip()) > 0:
                try:
                    protocol, ip, age, mac, arp_type, interface = line.split(maxsplit=6)
                    ip = ip.strip('()')  # Remove parentheses around IP address

                    logger.info("Processed {}".format(host))
                    macvendor = get_macvendor(mac)
                    vlan = ""

                    result.append({"ip": ip, "vlan": vlan, "protocol": protocol, "age": age, "mac": mac, "macvendor": macvendor, "arp_type": arp_type, "interface": interface})

                except ValueError:
                    logger.error("Invalid ARP line for {}".format(host))
        elif process_type == "cam":
            if line.strip().startswith("Mac Address") or line.strip().startswith("Vlan"):
                continue
            elif line.strip().startswith("----"):
                continue
            elif len(line.strip()) > 0:
                try:
                    vlan, mac, arp_type, port = line.split(maxsplit=4)
                    logger.info("Processed {}".format(host))
                    macvendor = get_macvendor(mac)
                    protocol = ""
                    age = ""
                    interface = port
                    ip = ""

                    result.append({"ip": ip, "vlan": vlan, "protocol": protocol, "age": age, "mac": mac, "macvendor": macvendor, "arp_type": arp_type, "interface": interface})

                except ValueError:
                    logger.error("Invalid CAM line for {}".format(host))
        elif process_type == "linuxarp":
            if line.strip().startswith("Address") or line.strip().startswith("Vlan") or line.strip().startswith("Mac Address Table"):
                continue
            elif "(incomplete)" in line:
                continue
            elif line.strip().startswith("----"):
                continue
            elif len(line.strip()) > 0:
                try:
                    ip, arp_type, mac, flags, interface = line.split(maxsplit=5)
                    logger.info("Processed {}".format(host))
                    macvendor = get_macvendor(mac)
                    protocol = ""
                    age = ""
                    vlan = ""

                    result.append({"ip": ip, "vlan": vlan, "protocol": protocol, "age": age, "mac": mac, "macvendor": macvendor, "arp_type": arp_type, "interface": interface})

                except ValueError:
                    logger.error("Invalid Linux ARP line for {}".format(host))
    return result


def get_macvendor(mac):
    '''
        Lookup a MAC if it's associated with a vendor
    '''
    macvendor = "Unknown"
    macvendors_api_url = "https://api.macvendors.com/"
    try:
        macvendors_request = requests.get(macvendors_api_url + mac, headers={'user-agent': "security-screening"})
        time.sleep(1)       # Avoid time outs
        if macvendors_request.status_code == 200:
            response = macvendors_request.text
            if response:
                macvendor = response

    except:
        print("Unable to do macvendor query")
    logger.info("MAC vendor {} for {}".format(macvendor, mac))
    return macvendor.strip()


def create_arp_table(hosts_output):
    logger.info("Creating output table")
    arp_output_table = PrettyTable()
    arp_output_table.field_names = ["System", "VLAN", "IP", "MAC", "MAC vendor", "Age", "Interface"]
    arp_output_table.align["System"] = "l"
    arp_output_table.align["IP"] = "l"
    arp_output_table.align["MAC"] = "l"
    arp_output_table.align["MAC vendor"] = "l"
    for host in hosts_output:
        for entry in hosts_output[host]:
            arp_output_table.add_row([host, entry["vlan"], entry["ip"], entry["mac"], entry["macvendor"], entry["age"], entry["interface"]])

    return arp_output_table


def save_output(output_file, old_output_file, arp_output_table):
    logger.info("Saving output")
    try:
        shutil.copy(output_file, old_output_file)
    except FileNotFoundError:
        logger.info("Error: {} not found.".format(output_file))
    except Exception as e:
        logger.error("Error when writing {} {}.".format(output_file, str(e)))
    with open(output_file, "w") as file:
        file.write(arp_output_table)


def compare_output(old_output_file, output_file):
    logger.info("Comparing with previous output")
    try:
        with open(output_file, "r") as file1, open(old_output_file, "r") as file2:
            lines1 = file1.readlines()
            lines2 = file2.readlines()
            differ = difflib.Differ()
            diff = list(differ.compare(lines1, lines2))

            for line in diff:
                if line.startswith("+ ") or line.startswith("- "):
                    if "-----------------" in line:
                        continue
                    elif "System" in line:
                        continue
                    else:
                        print(line.strip())            
    except FileNotFoundError:
        logger.error("Error: One or both files not found.")
    except Exception as e:
        logger.error("Error when diffing {}.".format(str(e)))


if __name__ == "__main__":
    '''
        Configuration
    '''
    default_command = "arp -n"  # alternative is "arp" or "cam"
    default_username = "koenv"
    default_password = "koenv"
    default_process_type = "arp"

    hosts = {"192.168.171.176": {"details": {"username": default_username, "password": default_password, "command": default_command, "process_type": "linuxarp"},
                                 "output": False},
             "192.168.171.174": {"details": {"username": default_username, "password": default_password, "command": default_command, "process_type": "cam"},
                                 "output": False},
             }

    logfile = "hardware-inventory.log"
    output_file = "hardware-inventory-ssh.txt"

    '''
        Create logger object
    '''
    logger = logging.getLogger('hardware-inventory')
    logger.setLevel(logging.DEBUG)
    ch = logging.FileHandler(logfile, mode='a')
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    ConsoleOutputHandler = logging.StreamHandler()
    logger.addHandler(ConsoleOutputHandler)

    '''
        Output stored in hosts_output
    '''
    hosts_output = {}

    '''
        Start
    '''
    logger.info("Start inventory")
    for ssh_client in hosts:
        if len(hosts[ssh_client]["details"].get("username".strip(), "")) > 0:
            username = hosts[ssh_client]["details"]["username"].strip()
        else:
            username = input("What is the username for {}? ".format(ssh_client)).strip()
        if len(hosts[ssh_client]["details"].get("password".strip(), "")) > 0:
            password = hosts[ssh_client]["details"]["password"].strip()
        else:
            password = getpass.getpass("What is the password for {}? (will not display): ".format(ssh_client)).strip()
        if len(hosts[ssh_client]["details"].get("command".strip(), "")) > 0:
            command = hosts[ssh_client]["details"]["command"].strip()
        else:
            command = input("What is the command for {}? ".format(ssh_client)).strip()

        result = handle_client(ssh_client, username, password, command)
        if hosts[ssh_client]["details"]["process_type"] == "cam":
            result = result_cisco_cam

        if result:
            hosts[ssh_client]["output"] = result
            logger.info("Got result for {}".format(ssh_client))
        else:
            logger.info("No result for {}".format(ssh_client))

        result = process_client(ssh_client, hosts[ssh_client]["output"], hosts[ssh_client]["details"]["process_type"])
        for value in result:
            if ssh_client in hosts_output:
                hosts_output[ssh_client].append(value)
            else:
                hosts_output[ssh_client] = [value]

    arp_output_table = create_arp_table(hosts_output)
    save_output(output_file, "{}.old".format(output_file), arp_output_table.get_string())
    compare_output(output_file, "{}.old".format(output_file))
    logger.info("End inventory")
