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

        skip_first = False
        with open(file_system, "r", encoding=encoding) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if (type(row) == list and len(row) < 1):
                     skip_first = True
                     break
        with open(file_system, "r", encoding=encoding) as csvfile:
            if skip_first:
                next(csvfile)
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
                elif 'System Up Time' in row:
                    audit_osbootdate = row['System Up Time']         

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
                elif 'System type' in row:
                    audit_ostype = row['System type']

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
                else:
                    audit_mem_virt = ""

                if 'Hotfix(s)' in row:               
                    audit_hotfix = row['Hotfix(s)']
                elif 'Hotfix(es)' in row:
                    audit_hotfix = row['Hotfix(es)']  

    try:
        if len(audit_hostname) > 0:
            True
    except UnboundLocalError:
        print("Opening as non-dict")
        with open(file_system, 'r', encoding='cp1252') as csv_file:            
            csv_reader = csv.reader(csv_file)
            skip_first = True
            for row in csv_reader:
                if skip_first:
                    skip_first = False
                    continue
                audit_hostname = row[0].encode('utf-8').decode('utf-8')
                audit_domain = row[28].encode('utf-8').decode('utf-8')
                audit_os_name = row[1].encode('utf-8').decode('utf-8')
                audit_osversion = row[2].encode('utf-8').decode('utf-8')
                audit_biosversion = row[15].encode('utf-8').decode('utf-8')
                audit_productid = row[9].encode('utf-8').decode('utf-8')
                audit_owner = row[6].encode('utf-8').decode('utf-8')
                audit_system_locale = row[19].encode('utf-8').decode('utf-8')
                audit_input_locale = row[20].encode('utf-8').decode('utf-8')
                audit_timezone = row[21].encode('utf-8').decode('utf-8')
                audit_logon = row[29].encode('utf-8').decode('utf-8')
                audit_osconfiguration = row[4].encode('utf-8').decode('utf-8')
                audit_osinstalldate = row[10].encode('utf-8').decode('utf-8')
                audit_osbootdate = row[11].encode('utf-8').decode('utf-8')
                audit_osmanufact = row[12].encode('utf-8').decode('utf-8')
                audit_osmodel = row[12].encode('utf-8').decode('utf-8')
                audit_ostype = ""
                audit_cpu = row[14].encode('utf-8').decode('utf-8')
                audit_sysdir = row[17].encode('utf-8').decode('utf-8')
                audit_windir = row[16].encode('utf-8').decode('utf-8')
                audit_bootdevice = row[18].encode('utf-8').decode('utf-8')
                audit_mem_phys = row[22].encode('utf-8').decode('utf-8')
                audit_mem_virt = row[23].encode('utf-8').decode('utf-8')
                audit_hotfix = row[30].encode('utf-8').decode('utf-8')

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

    if es:
        es.index(index=config["elasticsearch_index"], document=systeminfo)
    else:
        print("\nCSC - 1 - Inventory and Control of Hardware Assets\n-------------------------------------------------------")
        print("{}\t{}\t{} {}\t{}\t{}\t{}".format(systeminfo["hostname"], systeminfo["domain"], systeminfo["os_name"], systeminfo["os_version"], systeminfo["os_model"], systeminfo["system_owner"], systeminfo["timezone"]))
    
    return audit_hostname

def user_accounts(config, es, asset_dir, audit_hostname, dnq=False):
    file_users = asset_dir + "/users_detail.txt"
    user_accounts = []
    if os.path.exists(file_users):
        if dnq:
            rawdata=open(file_users,"rb").read()
            encoding = chardet.detect(rawdata)["encoding"]
            file = open(file_users, "r", encoding=encoding)
            for line_code in  file.readlines():
                line = line_code.encode('utf-8')
                if "Nom d'utilisateur" in line.decode('utf-8'):
                    username = line[29:].rstrip().lstrip()
                if "Commentaire" in line.decode('utf-8'):
                    comment = line[29:].rstrip().lstrip()
                if ": actif" in line.decode('utf-8'):
                    active = line[29:].decode('utf-8').rstrip().lstrip().replace("Oui", "Yes").replace("Non", "No").encode('utf-8')
                if ": dernier changmt" in line.decode('utf-8'):
                    pwlastset = line[32:].decode('utf-8').rstrip().lstrip().replace("Jamais", "Never").encode('utf-8')
                if "Le mot de passe expire" in line.decode('utf-8'):
                    expires = line[29:].decode('utf-8').rstrip().lstrip().replace("Jamais", "Never").encode('utf-8')
                if "Dernier acc" in line.decode('utf-8'):
                    lastlogon = line[29:].decode('utf-8').rstrip().lstrip().replace("Jamais", "Never").encode('utf-8')
                if "Appartient aux groupes locaux" in line.decode('utf-8'):
                    local_group = line[29:].decode('utf-8').rstrip().lstrip().replace("*","").encode('utf-8')
                if "Appartient aux groupes globaux" in line.decode('utf-8'):
                    global_group = line[29:].decode('utf-8').rstrip().lstrip().replace("*","").replace("None","").encode('utf-8')
                if "La commande s'est termin" in line.decode('utf-8'):
                    if username:
                        user_accounts.append( [username, comment, active, expires, lastlogon, local_group, global_group, pwlastset] )
                        username=""
                        comment=""
                        active=""
                        expires=""
                        lastlogon=""
                        local_group=""
                        global_group=""
                        pwlastset=""
        else:
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
                        user_accounts.append( [username, comment, active, expires, lastlogon, local_group, global_group, pwlastset] )
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
                rawdata=open(file_users_backup,"rb").read()
                encoding = chardet.detect(rawdata)["encoding"]
                file = open(file_users_backup, "r", encoding=encoding)
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

    if not es:
        print("\nCSC 5 - Account Management\n-------------------------------------------------------")

    for el in user_accounts:
        if dnq:
            el[0] = el[0].decode('utf-8')
            el[1] = el[1].decode('utf-8')
            el[2] = el[2].decode('utf-8')
            el[3] = el[3].decode('utf-8')
            el[4] = el[4].decode('utf-8')
            el[5] = el[5].decode('utf-8')
            el[6] = el[6].decode('utf-8')
            el[7] = el[7].decode('utf-8')
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
                "global_group": el[6],
                "password_last_set": el[7]
        }
        if es:
                es.index(index=config["elasticsearch_index"], document=user)
        else:
            print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(audit_hostname, user["username"], user["active"], user["password_last_set"], user["expires"], user["last_logon"], user["local_group"]))

def software_list(config, es, asset_dir, audit_hostname, dnq=False):
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

        skip_first = False
        with open(file_softwarelist, "r", encoding=encoding) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if (type(row) == list and len(row) < 1):
                     skip_first = True
                     break

        with open(file_softwarelist, "r", encoding=encoding) as csvfile:
            if skip_first:
                next(csvfile)
            reader = csv.DictReader(csvfile, fieldnames=["Node", "AssignmentType", "Caption"])
            for row in reader:
                if 'Caption' in row and row["Caption"] != "Caption" and row["Caption"] not in software_list and row["Caption"] not in config["ignore_software"] and row["Caption"] is not None:
                    res = list(filter(lambda x: x in row["Caption"],config["ignore_software"]))
                    if not len(res) > 0:
                        software_list.append(row["Caption"].strip())

    if not es:
        print("\nCSC - 2 - Inventory and Control of Software Assets\n-------------------------------------------------------")
        print("{}\n".format(audit_hostname))
    for el in software_list:
        software = {
                "timestamp": datetime.datetime.now(),
                "screening_session": config["screening_session"],
                "screening_type": "software",    
                "hostname": audit_hostname,
                "software": el
        }
        if es:
            es.index(index=config["elasticsearch_index"], document=software)
        else:
            if dnq:
                print("{}".format(el.encode('utf-8')))
            else:
                print("{}".format(el))
            

def anti_virus(config, es, asset_dir, audit_hostname, dnq=False):
    file_av_settings = asset_dir + "/tasklist.csv"
    audit_antimalware = [ "n/a", "n/a" ]
    if os.path.exists(file_av_settings):


        if dnq:
            encoding='cp1252'
            with open(file_av_settings,"r", encoding=encoding) as csvfile:
                csv_reader = csv.reader(csvfile)
                skip_first = True       
                for row in csv_reader:
                    if skip_first:
                        skip_first = False
                        continue

                    image_name = row[0].encode('utf-8').decode('utf-8')
                    if image_name in config["antimalware_software"]:
                        audit_antimalware = [ image_name, row[1]]
                        
        else:        
            rawdata=open(file_av_settings,"rb").read()
            encoding = chardet.detect(rawdata)["encoding"]

            skip_first = False
            with open(file_av_settings, "r", encoding=encoding) as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if (type(row) == list and len(row) < 1):
                        skip_first = True
                        break

            with open(file_av_settings, "r", encoding=encoding) as csvfile:
                if skip_first:
                    next(csvfile)
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

    if es:                
        es.index(index=config["elasticsearch_index"], document=anti_malware)
    else:
        print("\nCSC - 10 - Malware Defenses\n-------------------------------------------------------")
        print("{}\t{}".format(audit_hostname, anti_malware["anti_malware"]))

def listening_services(config, es, asset_dir, audit_hostname, dnq = False):
    file_netstat = asset_dir + "/netstat.txt"
    file_tasklist = asset_dir + "/tasklist.csv"
    listening_apps = []
    
    if os.path.exists(file_netstat):
        rawdata=open(file_netstat,"rb").read()
        encoding = chardet.detect(rawdata)["encoding"]
        if dnq:
            encoding='utf-8'
        file = open(file_netstat, "r", encoding=encoding, errors='replace') 
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

                        skip_first = False
                        if dnq:
                            encoding='cp1252'
                            with open(file_tasklist,"r", encoding=encoding) as csvfile:
                                csv_reader = csv.reader(csvfile)
                                skip_first = True       
                                for row in csv_reader:
                                    if skip_first:
                                        skip_first = False
                                        continue
                                    if row[1].encode('utf-8').decode('utf-8') == pid:
                                        image_name = row[0].encode('utf-8').decode('utf-8')                                
                                        session_name = row[0].encode('utf-8').decode('utf-8')                                
                                        if session_name == "":
                                                session_name = "Services"
                                        user_name = row[6].encode('utf-8').decode('utf-8')                                
                                        application = lookup_application(port, image_name, session_name)
                                        listening_apps.append([port, pid, image_name, session_name, user_name, application])                            
                        else:
                            with open(file_tasklist, "r", encoding=encoding) as csvfile:
                                reader = csv.reader(csvfile)
                                for row in reader:
                                    if (type(row) == list and len(row) < 1):
                                        skip_first = True
                                        break
                            encoding='utf-8'
                            with open(file_tasklist,"r", encoding=encoding) as csvfile:
                                if skip_first:
                                    next(csvfile)
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

    if not es:
        print("\nCSC - 3 - Secure Configuration of Hardware Assets and Software\n-------------------------------------------------------")

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
        if es:
            es.index(index=config["elasticsearch_index"], document=listening)            
        else:
            if dnq:
                print("{}\ttcp/{}\t{}\t{}\t{}\t{}\t".format(audit_hostname, listening["port"], listening["image_name"].encode('utf-8'), listening["user_name"].encode('utf-8'), listening["session_name"], listening["application"].encode('utf-8')))
            else:
                print("{}\ttcp/{}\t{}\t{}\t{}\t{}\t".format(audit_hostname, listening["port"], listening["image_name"], listening["user_name"], listening["session_name"], listening["application"]))
            