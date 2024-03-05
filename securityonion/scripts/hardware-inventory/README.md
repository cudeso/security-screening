# Hardware inventory based on audit data

Build the hardware inventory table based on **arp** files (created on Windows, Linux or OSX). 

Use `get-macaddrs-fromaudit.py` to 
1. Read `arp.txt`, either created via [auditscript.bat](https://github.com/cudeso/security-screening/blob/master/auditscript.bat) or by manually running `arp -a`
2. Query [macvendors.com](https://macvendors.com) for each MAC address
3. Print out pretty table

```
+--------+---------------+-------------------+-----------------------+
| System | IP            | MAC               | MAC vendor            |
+--------+---------------+-------------------+-----------------------+
| local  | 192.168.1.50  | 00:00:00:00:00:00 | Cisco-Linksys, LLC    |
| local  | 192.168.1.10  | 00:00:00:00:00:00 | Synology Incorporated |
| local  | 192.168.1.22  | 00:00:00:00:00:00 | Apple, Inc.           |
+--------+---------------+-------------------+-----------------------+
```

# Hardware inventory based on switch connected devices

Build the hardware inventory table based on the **CAM** table of Rockwell / Allen Bradley Stratix switches. This corresponds with `sh mac address-table` and displays the MAC address of the devices detected at L2 (IP-layer). Tested on Stratix 5700 Switches.

Unfortunately, Stratix switches do not (?) support obtaining the IP addresses from L3 (similar as running the `sh arp`). None of the Cisco MIBs for getting the IPs returned usable results.

Works with **Linux** (`snmpwalk_windows=False`) or with **Windows**, via SnmpWalk.exe (`snmpwalk_windows=True`).

Usage:
1. In `switch-hardware-inventory.py` update `switches` with the list of switches and their SNMP community string
2. The script will query for all detected VLANs. Keep in mind that VLANs 1002-1005 are internal Cisco VLANs.
3. It then obtains the MAC address table, the bridge port numbers and the ifindex mapping
4. Query [macvendors.com](https://macvendors.com) for each MAC address
5. Print out pretty table

```
+---------------+------+----+-------------------+--------------------+------+-----------+
| System        | VLAN | IP | MAC               | MAC vendor         | Port | Interface |
+---------------+------+----+-------------------+--------------------+------+-----------+
| 111.22.111.22 |  5   |    | 00 00 00 00 00 00 | Cisco Systems, Inc |  0   |           |
| 111.22.111.22 |  3   |    | 00 00 00 00 00 00 | Cisco Systems, Inc | 1111 |           |
| 111.22.111.22 |  2   |    | 00 00 00 00 00 00 | Cisco Systems, Inc | 1112 |    Po44   |
| 111.22.111.22 |  2   |    | 00 00 00 00 00 00 | Cisco Systems, Inc | 1113 |           |
| 111.22.111.22 |  2   |    | 00 00 00 00 00 00 | Cisco Systems, Inc | 1114 |    Po2    |
+---------------+------+----+-------------------+--------------------+------+-----------+
```

# Hardware inventory retrieved via an SSH login to a switch

Build the hardware inventory table based on the output of command executed via SSH.

Use `switch-hardware-inventory-ssh.py` to

1. Login to each hosts defined in the variable `hosts`
2. Execute the command (`command`). Either use the credentials stored in `hosts` or ask the user to type in the credentials
3. Parse the output of the command
4. Save the output to `hardware-inventory-ssh.txt`
5. Compare the output with the previous execution and highlight the differences.

Update the variable `hosts` with your host details. Add an entry with
- IP address
  - A dictionary with `details`. If you leave `username`, `password`, or `command` empty then the script will ask you for the input
    - Processtype can be `arp` (Cisco ARP), `cam` (Cisco CAM) or `linuxarp` (Linux - Ubuntu ARP)
  - A variable `output`
```
"192.168.171.176": {"details": {"username": default_username, "password": default_password, "command": default_command, "process_type": "linuxarp"},
                    "output": False}
```

The script will connect via SSH to each IP and execute the command. The output of the command is then parsed and saved in a table in `hardware-inventory-ssh.txt`. It then compares the output with the previous execution. This immediately gives a diff compared to a previous run.

Example output of `hardware-inventory-ssh.txt`
```
+-----------------+------+---------------+-------------------+---------------------------------+-----+-----------+
| System          | VLAN | IP            | MAC               | MAC vendor                      | Age | Interface |
+-----------------+------+---------------+-------------------+---------------------------------+-----+-----------+
| 192.168.171.176 |      | 192.168.171.1 | 3e:22:fb:72:8c:69 | Unknown                         |     |   ens33   |
| 192.168.171.176 |      | 192.168.171.2 | 00:50:56:e6:0a:63 | VMware, Inc.                    |     |   ens33   |
| 192.168.171.174 |  1   |               | 001b.5400.33c0    | Cisco Systems, Inc              |     |  Gi1/0/1  |
| 192.168.171.174 |  1   |               | 0024.2bb6.fd30    | Hon Hai Precision Ind. Co.,Ltd. |     |  Gi1/0/2  |
+-----------------+------+---------------+-------------------+---------------------------------+-----+-----------+
```

Obtaining the ARP table on a Cisco switch: `show arp` returns this output

```
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.1.10     -          001b.5400.33c0  ARPA   Vlan1
Internet  192.168.1.4      2          0024.2bb6.fd30  ARPA   Vlan1
```

Obtaining the CAM table on a Cisco switch: `show mac address-table dynamic` returns this output

```
Mac Address Table
-------------------------------------------
Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
  1    001b.5400.33c0     DYNAMIC     Gi1/0/1
  1    0024.2bb6.fd30     DYNAMIC     Gi1/0/2
```

Use of pub/private key authentication is foreseen in a next version.