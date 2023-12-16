import subprocess
import re
import json
import sys
import logging
import os
import requests
import time
from prettytable import PrettyTable


def snmpwalk(community, hostname, oid, snmpwalk_write_result, snmpwalk_windows, encoding="utf-8"):
    try:
        logger.info("Start with SNMP walk for {}".format(oid))
        if snmpwalk_windows:
            logger.info("Using SnmpWalk.exe (windows)")
            oid_stop = "{}.65535".format(oid)
            if os.path.isfile("SnmpWalk.exe"):
                snmpwalk_output = subprocess.check_output(
                    ["./SnmpWalk.exe", "-v:2c", "-c:{}".format(community), "-r:{}".format(hostname),
                     "-os:{}".format(oid), "-op:{}".format(oid_stop)])
                snmpwalk_output = snmpwalk_output.decode("utf-8").split("\r\n")
            else:
                logger.error("SnmpWalk.exe not found")
                snmpwalk_output = False
        else:
            logger.info("Using snmpwalk (linux)")
            snmpwalk_output = subprocess.check_output(['snmpwalk', '-c', community, '-v', '2c', hostname, oid],
                                                      universal_newlines=True, encoding=encoding)
            snmpwalk_output = snmpwalk_output.splitlines()
        logger.info("End SNMP walk")
        if snmpwalk_write_result:
            with open(oid, "a") as file:
                if isinstance(snmpwalk_output, list):
                    file.write(''.join(snmpwalk_output))
                else:
                    file.write(snmpwalk_output)

            # disable for production
            for line in snmpwalk_output:
                logger.debug(line)
    except subprocess.TimeoutExpired:
        snmpwalk_output = False
        logger.error("Timeout when executing snmpwalk for {} {}".format(hostname, oid))
    except subprocess.CalledProcessError:
        snmpwalk_output = False
        logger.error("CalledProcessError when executing snmpwalk for {} {}".format(hostname, oid))
    except:
        snmpwalk_output = False
        logger.error("Problem when executing snmpwalk for {} {}".format(hostname, oid))

    return snmpwalk_output


def process_switch(switch, snmpwalk_write_result=False, snmpwalk_windows=False, encoding="utf-8", max_vlans=9999):
    vlans = []
    bridge_ports = {}

    logger.info("Process {}".format(switch))
    host = switch["host"]
    community_string = switch["community_string"]

    # Step 1: Retrieve the VLANs
    vlans_output = snmpwalk(community_string, host, vtpVlanState, snmpwalk_write_result, snmpwalk_windows, encoding)
    if vlans_output:
        # Extract the VLANs
        for line in vlans_output:
            vlan_id = False
            if snmpwalk_windows:
                if vtpVlanState in line and "Type=Integer" in line:
                    vlan_id = line.split(", Type=Integer")[0].split(".1.")
                    vlan_id = vlan_id[len(vlan_id) - 1]
            elif "vtpVlanState" in line:
                vlan_id = line.split("vtpVlanState")[1].split("= INTEGER:")[0].split(".1.")[1].strip()
            elif vtpVlanState_match in line:
                vlan_id = line.split("= INTEGER:")[0].split(".1.")
                vlan_id = vlan_id[len(vlan_id) - 1]
            if vlan_id:
                vlan_id = int(vlan_id)
                logger.info("Found VLAN {}".format(vlan_id))
                if vlan_id not in vlans:
                    vlans.append(vlan_id)
            if vlan_id > max_vlans:
                logger.error("Maximum VLAN query reached {}".format(max_vlans))
                break
    else:
        return False

    if len(vlans) < 1:
        logger.error("No VLANs found.")
        return False

    # Step 2: For each VLAN: get the MAC address table, the bridge port numbers and the ifindex mapping
    for vlan in vlans:
        logger.info("Working with VLAN {}".format(vlan))
        community_string = "{}@{}".format(community_string, vlan)

        mac_address_table = snmpwalk(community_string, host, dot1dTpFdbAddress, snmpwalk_write_result, snmpwalk_windows,
                                     encoding)
        if mac_address_table:
            for line in mac_address_table:
                bridge_port = False
                if dot1dTpFdbAddress or dot1dTpFdbAddress_match in line:
                    if "Hex-STRING" in line:
                        mac_addr = line.split("= Hex-STRING:")[1].strip()
                        bridge_port = line.split("= Hex-STRING:")[0].strip().split(dot1dTpFdbAddress_match)[1]
                    elif "OctetString" in line:
                        mac_addr = line.split(", Type=OctetString, Value=")[1].strip()
                        bridge_port = \
                        line.split(", Type=OctetString, Value=")[0].strip().split(dot1dTpFdbAddress_match)[1]
                if bridge_port and bridge_port not in bridge_ports:
                    logger.info("Found MAC {} at bridge port {}".format(mac_addr, bridge_port))
                    bridge_ports[bridge_port] = {"vlan": vlan_id, "mac": mac_addr}

        bridge_port_numbers = snmpwalk(community_string, host, dot1dTpFdbPort, snmpwalk_write_result, snmpwalk_windows,
                                       encoding)
        if bridge_port_numbers:
            for line in bridge_port_numbers:
                bridge_port_number = False
                bridge_port = False
                if dot1dTpFdbPort or dot1dTpFdbPort_match in line:
                    if "INTEGER" in line:
                        bridge_port_number = line.split("= INTEGER:")[1].strip()
                        bridge_port = line.split("= INTEGER:")[0].strip().split(dot1dTpFdbPort_match)[1]
                    elif "Integer" in line:
                        bridge_port_number = line.split(", Type=Integer, Value=")[1].strip()
                        bridge_port = line.split(", Type=Integer, Value=")[0].strip().split(dot1dTpFdbPort_match)[1]
                if bridge_port_number:
                    logger.info("Found bridge port number: {} for bridge port {}".format(bridge_port_number,
                                                                                         bridge_port))
                    if bridge_ports.get(bridge_port, False):
                        bridge_ports[bridge_port]["port_number"] = bridge_port_number
                    else:
                        bridge_ports[bridge_port] = {"port_number": bridge_port_number}

        ifindex_mappings = snmpwalk(community_string, host, dot1dBasePortIfIndex, snmpwalk_write_result,
                                    snmpwalk_windows, encoding)
        if ifindex_mappings:
            for line in ifindex_mappings:
                ifindex = False
                tmp_bridge_port = False
                bridge_port = False
                if dot1dBasePortIfIndex or dot1dBasePortIfIndex_match in line:
                    if "INTEGER" in line:
                        ifindex = line.split("= INTEGER:")[1].strip()
                        tmp_bridge_port = line.split("= INTEGER:")[0].strip().split(dot1dBasePortIfIndex_match)[1][1:]
                    elif "Type=Integer" in line:
                        ifindex = line.split(", Type=Integer, Value=")[1].strip()
                        tmp_bridge_port = \
                        line.split(", Type=Integer, Value=")[0].strip().split(dot1dBasePortIfIndex_match)[1][1:]
                if tmp_bridge_port:
                    for b_port in bridge_ports:
                        if bridge_ports[b_port].get("port_number", False) == tmp_bridge_port:
                            bridge_port = b_port
                if bridge_port and ifindex:
                    logger.info("Found ifindex: {} for bridge port {}".format(ifindex, bridge_port))
                    if bridge_ports.get(bridge_port, False):
                        bridge_ports[bridge_port]["ifindex"] = ifindex
                    else:
                        bridge_ports[bridge_port] = {"ifindex": ifindex}

        ifnames_mappings = snmpwalk(community_string, host, ifName, snmpwalk_write_result, snmpwalk_windows, encoding)
        if ifnames_mappings:
            for line in ifnames_mappings:
                ifname_map = False
                tmp_bridge_port = False
                bridge_port = False
                if ifName or ifName_match in line:

                    if "IF-MIB::ifName" in line:
                        line = line.replace("IF-MIB::ifName", ifName)
                    if "STRING" in line:
                        ifname_map = line.split("= STRING:")[1].strip()
                        tmp_bridge_port = line.split("= STRING:")[0].strip().strip().split(ifName_match)[1][1:]
                    elif "OctetString" in line:
                        ifname_map = line.split(", Type=OctetString, Value=")[1].strip()
                        tmp_bridge_port = \
                        line.split(", Type=OctetString, Value=")[0].strip().strip().split(ifName_match)[1][1:]
                if tmp_bridge_port:
                    for b_port in bridge_ports:
                        if bridge_ports[b_port].get("ifindex", False) == tmp_bridge_port:
                            bridge_port = b_port
                if bridge_port and ifname_map:
                    logger.info("Found ifname: {} for bride port {}".format(ifname_map, tmp_bridge_port))
                    if bridge_ports.get(bridge_port):
                        bridge_ports[bridge_port]["ifname"] = ifname_map
                    else:
                        bridge_ports[bridge_port] = {"ifname": ifname_map}

    return bridge_ports


def process_macvendors(bridge_ports):
    macvendors_api_url = "https://api.macvendors.com/"
    if len(bridge_ports) > 0:
        for port, port_details in bridge_ports.items():
            mac = port_details.get("mac", False)
            if mac:
                macvendor = "Unknown"
                try:
                    macvendors_request = requests.get(macvendors_api_url + mac,
                                                      headers={'user-agent': "security-screening"})
                    if macvendors_request.status_code == 200:
                        response = macvendors_request.text
                        if response:
                            macvendor = response
                except:
                    print("Unable to do macvendor query")
            bridge_ports[port]["macvendor"] = macvendor
    return bridge_ports

if __name__ == "__main__":
    vtpVlanState = ".1.3.6.1.4.1.9.9.46.1.3.1.1.2"
    vtpVlanState_match = ".9.9.46.1.3.1.1.2."
    dot1dTpFdbAddress = ".1.3.6.1.2.1.17.4.3.1.1"
    dot1dTpFdbAddress_match = ".17.4.3.1.1"
    dot1dTpFdbPort = ".1.3.6.1.2.1.17.4.3.1.2"
    dot1dTpFdbPort_match = ".17.4.3.1.2"
    dot1dBasePortIfIndex = ".1.3.6.1.2.1.17.1.4.1.2"
    dot1dBasePortIfIndex_match = ".17.1.4.1.2"
    ifName = ".1.3.6.1.2.1.31.1.1.1.1"
    ifName_match = ".31.1.1.1.1"

    logfile = "hardware-inventory.log"
    logger = logging.getLogger('hardware-inventory')
    logger.setLevel(logging.DEBUG)
    ch = logging.FileHandler(logfile, mode='a')
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    ConsoleOutputHandler = logging.StreamHandler()
    logger.addHandler(ConsoleOutputHandler)

    switches = [{"host": "192.168.171.176", "community_string": "public"}]

    logger.info("Start inventory")
    for switch in switches:
        bridge_ports = process_switch(switch, snmpwalk_write_result=True, snmpwalk_windows=False, encoding="cp850", max_vlans=4)
        bridge_ports = process_macvendors(bridge_ports)

        arp_output_table = PrettyTable()
        arp_output_table.field_names = ["System", "VLAN", "IP", "MAC", "MAC vendor", "Port", "Interface"]
        arp_output_table.align["System"] = "l"
        arp_output_table.align["IP"] = "l"
        arp_output_table.align["MAC"] = "l"
        arp_output_table.align["MAC vendor"] = "l"

        for port, bridge_port in bridge_ports.items():
            arp_output_table.add_row([switch["host"], bridge_port.get("vlan", ""), bridge_port.get("ip", ""), bridge_port.get("mac", ""), bridge_port.get("macvendor", ""),
                                        bridge_port.get("port_number", ""), bridge_port.get("ifname", "")])
        print(arp_output_table)
        #print(json.dumps(bridge_ports, indent=4))

    logger.info("End inventory")