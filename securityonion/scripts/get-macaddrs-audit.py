import os
import re
import requests
import time
from prettytable import PrettyTable

def search_file(directory, target_file):
    results = []
    for root, dirs, files in os.walk(directory):
        if target_file in files:
            results.append(os.path.join(root, target_file))
    return results


if __name__ == '__main__':
    from config import config
 
    arp_file = "arp.txt"
    macvendors_api_url = "https://api.macvendors.com/"

    ignore_ip_arp = ["224.0.", "255.255.", "127.0.0.1"]
    arp_audit_files = search_file(config["output_path"], arp_file)
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    mac_pattern = re.compile(r'([0-9a-fA-F]{2}(?:[:-][0-9a-fA-F]{2}){5})', re.IGNORECASE)

    arp_collection = {}
    arp_output_table = PrettyTable()
    arp_output_table.field_names = ["System", "IP", "MAC", "MAC vendor"]
    arp_output_table.align["System"] = "l"
    arp_output_table.align["IP"] = "l"
    arp_output_table.align["MAC"] = "l"
    arp_output_table.align["MAC vendor"] = "l"

    if len(arp_audit_files) > 0:
        for arp in arp_audit_files:

            if "audit_" in arp:
                systemname = arp.split("audit_")[1].split("/{}".format(arp_file))[0]
                with open(arp, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        ip_addr = ip_pattern.findall(line)
                        if len(ip_addr) > 0:
                            ip_addr = ip_addr[0]
                        mac = mac_pattern.findall(line)
                        if len(mac) > 0:
                            mac = mac[0]                        
                        skip_line = False
                        for ip_ignore in ignore_ip_arp:
                            if ip_ignore in ip_addr:
                                skip_line = True
                                break
                        if len(mac) != 17:
                            skip_line = True
                        if mac == "ff-ff-ff-ff-ff-ff":
                            skip_line = True
                        if not skip_line:
                            macvendor = "Unknown"
                            try:
                                macvendors_request = requests.get(macvendors_api_url + mac, headers={'user-agent': "security-screening"})
                                macvendor = ""
                                if macvendors_request.status_code == 200:
                                    response = macvendors_request.text
                                    if response:
                                        macvendor = response
                            except:
                                print("Unable to do macvendor query")
                            #print(systemname, ip_addr, mac, macvendor)
                            arp_output_table.add_row([systemname, ip_addr, mac, macvendor])
                            time.sleep(1)
    print(arp_output_table)
