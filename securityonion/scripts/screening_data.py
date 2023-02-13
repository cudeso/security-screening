import os, json, sys
import datetime
import time
import chardet, csv

from screening_helpers import *

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def screening_system_name(config, es, asset_dir):
    file_system = asset_dir + "/systeminfo.csv"

    if os.path.exists(file_system):

        rawdata=open(file_system,"rb").read()
        encoding = chardet.detect(rawdata)["encoding"]
        asset_description = asset_dir.strip()

        with open(file_system, "r", encoding=encoding) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                if 'Host Name' in row:               
                    audit_hostname = row['Host Name']
                elif 'Host-naam' in row:
                    audit_hostname = row['Host-naam']

                if 'Domain' in row:               
                    audit_domain = row['Domain']
                elif 'Domein' in row:
                    audit_domain = row['Domein']

                if 'OS Name' in row:               
                    audit_os_name = row['OS Name']
                elif 'Naam van besturingssysteem' in row:
                    audit_os_name = row['Naam van besturingssysteem']

                if 'OS Version' in row:               
                    audit_osversion = row['OS Version']
                elif 'Versie van besturingssysteem' in row:
                    audit_osversion = row['Versie van besturingssysteem']

                if 'BIOS Version' in row:               
                    audit_biosversion = row['BIOS Version']
                elif 'BIOS-versie' in row:
                    audit_biosversion = row['BIOS-versie']

                if 'Product ID' in row:               
                    audit_productid = row['Product ID']
                elif 'Product-id' in row:
                    audit_productid = row['Product-id']

                if 'Registered Owner' in row:               
                    audit_owner = row['Registered Owner']
                elif 'Geregistreerde eigenaar' in row:
                    audit_owner = row['Geregistreerde eigenaar']

                if 'System Locale' in row:               
                    audit_system_locale = row['System Locale']
                elif 'Systeeminstellingen' in row:
                    audit_system_locale = row['Systeeminstellingen']

                if 'Input Locale' in row:               
                    audit_input_locale = row['Input Locale']
                elif 'Landinstellingen voor invoer' in row:
                    audit_input_locale = row['Landinstellingen voor invoer']

                if 'Time Zone' in row:               
                    audit_timezone = row['Time Zone']
                elif 'Tijdzone' in row:
                    audit_timezone = row['Tijdzone']

                if 'Logon Server' in row:               
                    audit_logon = row['Logon Server']
                elif 'Aanmeldingsserver' in row:
                    audit_logon = row['Aanmeldingsserver']

                if 'OS Configuration' in row:               
                    audit_osconfiguration = row['OS Configuration']
                elif 'Configuratie van besturingssysteem' in row:
                    audit_osconfiguration = row['Configuratie van besturingssysteem']

                if 'Original Install Date' in row:               
                    audit_osinstalldate = row['Original Install Date']
                elif 'Oorspronkelijke installatiedatum' in row:
                    audit_osinstalldate = row['Oorspronkelijke installatiedatum']

                if 'System Boot Time' in row:               
                    audit_osbootdate = row['System Boot Time']
                elif 'Systeemopstarttijd' in row:
                    audit_osbootdate = row['Systeemopstarttijd']                            

                if 'System Manufacturer' in row:               
                    audit_osmanufact = row['System Manufacturer']
                elif 'Computerfabrikant' in row:
                    audit_osmanufact = row['Computerfabrikant']    

                if 'System Model' in row:               
                    audit_osmodel = row['System Model']
                elif 'Computermodel' in row:
                    audit_osmodel = row['Computermodel']    

                if 'System Type' in row:               
                    audit_ostype = row['System Type']
                elif 'Type systeem' in row:
                    audit_ostype = row['Type systeem']    

                if 'Processor(s)' in row:               
                    audit_cpu = row['Processor(s)']
                elif 'Processor(s)' in row:
                    audit_cpu = row['Processor(s)']    

                if 'System Directory' in row:               
                    audit_sysdir = row['System Directory']
                elif 'Systeemmap' in row:
                    audit_sysdir = row['Systeemmap']    

                if 'Windows Directory' in row:               
                    audit_windir = row['Windows Directory']
                elif 'Windows-map' in row:
                    audit_windir = row['Windows-map']    

                if 'Boot Device' in row:               
                    audit_bootdevice = row['Boot Device']
                elif 'Opstartapparaat' in row:
                    audit_bootdevice = row['Opstartapparaat']    

                if 'Total Physical Memory' in row:               
                    audit_mem_phys = row['Total Physical Memory']
                elif 'Totaal fysiek geheugen' in row:
                    audit_mem_phys = row['Totaal fysiek geheugen']    

                if 'Virtual Memory: Available' in row:               
                    audit_mem_virt = row['Virtual Memory: Available']
                elif 'Virtueel geheugen: maximale grootte' in row:
                    audit_mem_virt = row['Virtueel geheugen: maximale grootte']                                                            

                if 'Hotfix(s)' in row:               
                    audit_hotfix = row['Hotfix(s)']
                elif 'Hotfix(es)' in row:
                    audit_hotfix = row['Hotfix(es)']  

    systeminfo = {
                "timestamp": datetime.datetime.now(),
                "screening_session": config["screening_session"],
                "screening_type": "systeminfo",    
                "hostname": audit_hostname,
                "domain": audit_domain,
                "os_name": audit_os_name,
                "os_version": audit_osversion,
                "bios_version": audit_biosversion,
                "productid": audit_productid,
                "system_owner": audit_owner,
                "system_locale": audit_system_locale,
                "input_locale": audit_input_locale,
                "timezone": audit_timezone,
                "logon": audit_logon,
                "os_configuration": audit_osconfiguration,
                "os_installdate": audit_osinstalldate,
                "os_bootdate": audit_osbootdate,
                "os_manufact": audit_osmanufact,
                "os_model": audit_osmodel,
                "os_type": audit_ostype,
                "cpu": audit_cpu,
                "sysdir": audit_sysdir,
                "windir": audit_windir,
                "bootdevice": audit_bootdevice,
                "mem_phys": audit_mem_phys,
                "mem_virt": audit_mem_virt,
                "hotfix": audit_hotfix
    }

    es.index(index=config["elasticsearch_index"], document=systeminfo)
    return audit_hostname

def user_accounts(config, es, asset_dir, audit_hostname):
    file_users = asset_dir + "/users_detail.txt"
    user_accounts = []
    if os.path.exists(file_users):
        rawdata=open(file_users,"rb").read()
        encoding = chardet.detect(rawdata)["encoding"]
        file = open(file_users, "r", encoding=encoding)
        for line in  file.readlines():
            if line[0:9] == "User name":
                username = line[29:].rstrip().lstrip()
            if line[0:7] == "Comment":
                comment = line[29:].rstrip().lstrip()
            if line[0:14] == "Account active":
                active = line[29:].rstrip().lstrip()
            if line[0:17] == "Password last set":
                pwlastset = line[29:].rstrip().lstrip()                        
            if line[0:16] == "Password expires":
                expires = line[29:].rstrip().lstrip()
            if line[0:10] == "Last logon":
                lastlogon = line[29:].rstrip().lstrip()
            if line[0:23] == "Local Group Memberships":
                local_group = line[29:].rstrip().lstrip().replace("*","")
            if line[0:24] == "Global Group memberships":
                global_group = line[29:].rstrip().lstrip().replace("*","").replace("None","")
            if line[0:34] == "The command completed successfully":

                if username:
                    user_accounts.append( [username, comment, active, expires, lastlogon, local_group, global_group] )
                    username=""
                    comment=""
                    active=""
                    expires=""
                    lastlogon=""
                    local_group=""
                    global_group=""
                    pwlastset=""
                    
        if (len(user_accounts) == 0):
            file_users_backup = asset_dir + "/net_user.txt"

            if os.path.exists(file_users_backup):
                file = open(file_users_backup, "r")
                for line in  file.readlines():
                    if line:
                        if line.find("-------------------------"):
                            if line.find("User accounts for"):
                                if line.find("The command completed su"):
                                    el = line.strip().split(" ")
                                    for e in el:
                                        if e:
                                            e = e.replace("\r\n","").strip()
                                            user_accounts.append( e )
                user_accounts.sort()

    for el in user_accounts:
        user= {
                "timestamp": datetime.datetime.now(),
                "screening_session": config["screening_session"],
                "screening_type": "accounts",    
                "hostname": audit_hostname,
                "username": el[0],
                "comment": el[1],
                "active": el[2],
                "expires": el[3],
                "last_logon": el[4],
                "local_group": el[5],
                "global_group": el[6]
        }
        es.index(index=config["elasticsearch_index"], document=user)

def software_list(config, es, asset_dir, audit_hostname):
    file_softwarelist = asset_dir + "/software_list.txt"
    software_list_raw = [] 
    software_list = []
    if os.path.exists(file_softwarelist):
        rawdata=open(file_softwarelist,"rb").read()
        encoding = chardet.detect(rawdata)["encoding"]
        #print("Open {} with encoding {}".format(file_softwarelist, encoding))
        file = open(file_softwarelist, "r", encoding=encoding)

        for line in  file.readlines():
            item = line.replace('"','').replace('\r\n','').strip()
            if item.find("==============="):
                if item not in software_list_raw:
                    software_list_raw.append(item)

                skip_item = False
                for ignore in config["ignore_software"]:
                    if item[:len(ignore)] == ignore:
                        skip_item = True

                res = list(filter(lambda x: x in item,config["ignore_software"]))
                if len(res) > 0:
                    skip_item = True

                if not skip_item:
                    if item not in software_list:
                        software_list.append(item.strip())

    file_softwarelist = asset_dir + "/software_list_wmic.csv"

    if os.path.exists(file_softwarelist):
        rawdata=open(file_softwarelist,"rb").read()
        encoding = chardet.detect(rawdata)["encoding"]
        #print("Open {} with encoding {}".format(file_softwarelist, encoding))

        with open(file_softwarelist, "r", encoding=encoding) as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=["Node", "AssignmentType", "Caption"])
            for row in reader:
                if 'Caption' in row and row["Caption"] != "Caption" and row["Caption"] not in software_list and row["Caption"] not in config["ignore_software"]:
                    res = list(filter(lambda x: x in row["Caption"],config["ignore_software"]))
                    if not len(res) > 0:
                        software_list.append(row["Caption"].strip())

    for el in software_list:
        software = {
                "timestamp": datetime.datetime.now(),
                "screening_session": config["screening_session"],
                "screening_type": "software",    
                "hostname": audit_hostname,
                "software": el
        }
        es.index(index=config["elasticsearch_index"], document=software)

def anti_virus(config, es, asset_dir, audit_hostname):
    file_av_settings = asset_dir + "/tasklist.csv"
    audit_antimalware = [ "n/a", "n/a" ]
    if os.path.exists(file_av_settings):
        rawdata=open(file_av_settings,"rb").read()
        encoding = chardet.detect(rawdata)["encoding"]

        with open(file_av_settings, "r", encoding=encoding) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'Image Name' in row:
                    if row['Image Name'] in config["antimalware_software"]:
                        audit_antimalware = [ row['Image Name'], row['PID'] ]
                else:
                    if row['Imagenaam'] in config["antimalware_software"]:
                        audit_antimalware = [ row['Imagenaam'], row['Proces-id'] ]

    anti_malware = {
                "timestamp": datetime.datetime.now(),
                "screening_session": config["screening_session"],
                "screening_type": "anti_malware",    
                "hostname": audit_hostname,
                "anti_malware": audit_antimalware[0]
        }
    es.index(index=config["elasticsearch_index"], document=anti_malware)

def listening_services(config, es, asset_dir, audit_hostname):
    file_netstat = asset_dir + "/netstat.txt"
    file_tasklist = asset_dir + "/tasklist.csv"
    listening_apps = []
    if os.path.exists(file_netstat):
        file = open(file_netstat, "r")
        linecount = 0
        for line in file.readlines():
            if linecount > 3:            
                line = line.strip('\r\n')
                source = line[8:22].rstrip().lstrip()
                if source[0:8] == "0.0.0.0:":
                    port = source[8:]
                    state = line[55:64].rstrip().lstrip()
                    if state == "LISTENING":
                        pid = line[71:].rstrip().lstrip()
                        rawdata=open(file_tasklist,"rb").read()
                        encoding = chardet.detect(rawdata)["encoding"]
                        with open(file_tasklist,"r", encoding=encoding) as csvfile:
                            reader = csv.DictReader(csvfile)
                            for row in reader:                        
                                if row['PID'] == pid:
                                    image_name = row['Image Name']
                                    session_name = row["Session Name"]
                                    if session_name == "":
                                        session_name = "Services"
                                    user_name = row["User Name"]
                                    application = lookup_application(port, image_name, session_name)
                                    listening_apps.append([port, pid, image_name, session_name, user_name, application])
            else:
                linecount = linecount + 1
    for el in listening_apps:
        listening = {
                "timestamp": datetime.datetime.now(),
                "screening_session": config["screening_session"],
                "screening_type": "listening_ports",    
                "hostname": audit_hostname,
                "port": el[0],
                "pid": el[1],
                "image_name": el[2],
                "session_name": el[3],
                "user_name": el[4],
                "application": el[5]
        }
        es.index(index=config["elasticsearch_index"], document=listening)            
