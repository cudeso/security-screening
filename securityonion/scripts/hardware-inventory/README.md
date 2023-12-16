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

