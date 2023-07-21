import sys
import os
from zipfile import ZipFile
import logging
import gzip
import shutil
from termcolor import colored
import subprocess
import hashlib
import chardet
import csv
import datetime
import time
import glob
import argparse
import time

from elasticsearch import Elasticsearch
from screening_mapping import screening_mapping
from screening_helpers import *

from screening_data import *

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import Evtx.Evtx as evtx
import Evtx.Views as e_views


def extract_zip(zipfile):
    if zipfile.lower()[len(zipfile)-4:] == ".zip":
        screening_zip = os.path.basename(zipfile)
        # full_path_to_zip = "{}/{}".format(config["input_path"], screening_zip)
        full_path_to_zip = zipfile
        full_output_path = "{}".format(config["output_path"])

        try:
            if os.path.exists("{}/{}".format(full_output_path, screening_zip[:len(screening_zip)-4])):
                logger.warning("Output path {} /{} already exists and will be overwritten".format(full_output_path, screening_zip[:len(screening_zip)-4]))
                print(colored("Output path {} /{} already exists and will be overwritten".format(full_output_path, screening_zip[:len(screening_zip)-4]), "red"))
            with ZipFile(full_path_to_zip, 'r') as zObject:
                zObject.extractall(path=full_output_path)
                logger.info("Extracted {} to {}".format(screening_zip, full_output_path))
                print(colored("Extracted {} to {}".format(screening_zip, full_output_path), "cyan"))

            return "{}/{}".format(full_output_path, screening_zip[:len(screening_zip)-4])
        except OSError as e:
            logger.error("File {} not found in {}".format(screening_zip, config["input_path"]))
            print(colored("File {} not found in {}".format(screening_zip, config["input_path"]), "red"))
            return False
        except BaseException as exception:
            logger.error(f"Exception Name: {type(exception).__name__}")
            logger.error(f"Exception Desc: {exception}")
            print(colored(f"Exception Name: {type(exception).__name__}"), "red")
            return False
    else:
        logger.error("No security screening ZIP file supplied.")
        print(colored("No security screening ZIP file supplied.", "red"))
        return False


def process_windows_logs(full_output_path, always_import=False, full_output_path_logs_dirflag=False):
    for el in config["evtx_logs_to_process"]:
        if full_output_path_logs_dirflag:
            # Remove everything after /output, use it first as a separator
            full_output_path = "{}/output".format(full_output_path.split("/output")[0])
            logger.info("Changing path to {}".format(full_output_path))
            full_output_path_logs_dir = full_output_path_logs_dirflag
        else:
            full_output_path_logs_dir = "logs"
        evtx_file = "{}/{}/{}".format(full_output_path, full_output_path_logs_dir, el)
        if os.path.isfile(evtx_file):
            if config.get("deletematchinglogs", False):
                deletematchinglogs(config, evtx_file)
            import_file = True
            md5hash = "000"
            logger.info("Processing {}".format(evtx_file))
            with open(evtx_file, "rb") as f:
                data = f.read()
                md5hash = hashlib.md5(data).hexdigest()
                full_path_existing_log = "{}{}".format(config["nsm_evtx"], md5hash)

            if md5hash in config["evtx_hashed_to_skip"]:
                import_file = False
            else:
                if os.path.exists(full_path_existing_log):
                    if always_import:
                        rm_command = "sudo rm -rf {}".format(full_path_existing_log)
                        os.system(rm_command)
                        logger.warning("Delete {}".format(full_path_existing_log))                        
                    else:
                        answer = input("The log {} has already been imported. Confirm re-import (with a risk of double events) with 'yes' or leave blank to skip. ".format(evtx_file))
                        if answer.lower() != "yes":
                            import_file = False
                        else:
                            rm_command = "sudo rm -rf {}".format(full_path_existing_log)
                            os.system(rm_command)
                            logger.warning("Delete {}".format(full_path_existing_log))
                            print(colored("Delete {}".format(full_path_existing_log), "red"))

            if import_file:
                subprocess.call(["sudo", config["so-import-evtx"], evtx_file])
                logger.info("Processed {}".format(evtx_file))
                print(colored("Processed {}".format(evtx_file), "cyan"))
            else:
                logger.warning("Skipping {} because already imported".format(evtx_file))
        else:
            logger.warning("Skipping {} as it does not exist".format(evtx_file))


def process_audit_files(full_output_path):

    if config["drop_es_index"]:
        logger.warning("Drop Elasticsearch index")
        elasticsearch.indices.delete(index=config["elasticsearch_index"], ignore_unavailable=True)
        logger.warning("Recreated Elasticsearch index")
        elasticsearch.indices.create(index=config["elasticsearch_index"], mappings=screening_mapping)

    try:
        logger.info("Audit files: system info for {}".format(full_output_path))
        print(colored("Audit files: system info for {}".format(full_output_path)))
        audit_hostname = screening_system_name(config, elasticsearch, full_output_path)

        logger.info("Audit files: user accounts for {}".format(audit_hostname))
        user_accounts(config, elasticsearch, full_output_path, audit_hostname)

        logger.info("Audit files: software list for {}".format(audit_hostname))
        software_list(config, elasticsearch, full_output_path, audit_hostname)

        logger.info("Audit files: AV for {}".format(audit_hostname))
        anti_virus(config, elasticsearch, full_output_path, audit_hostname)

        logger.info("Audit files: listening services for {}".format(audit_hostname))
        listening_services(config, elasticsearch, full_output_path, audit_hostname)

        return True

    except:
        logger.error("Error while parsing audit files for {}".format(full_output_path))
        print(colored("Error while parsing audit files for {}".format(full_output_path), "red"))
        return False


def process_chainsaw(full_output_path):
    selected_evtx_files = ""
    for el in config["evtx_logs_to_process"]:
        evtx_file = "{}/logs/{}".format(full_output_path, el)
        if os.path.isfile(evtx_file):
            selected_evtx_files = "{} \"{}\"".format(selected_evtx_files, evtx_file)

    if len(selected_evtx_files) > 0:
        chainsaw_outputh_path = "{}/chainsaw".format(full_output_path)
        chainsaw_comand = "{} hunt -s {} --mapping {} -r {} --csv --output {} {}".format(config["chainsaw_app"], config["chainsaw_sigma"], config["chainsaw_mappings"], config["chainsaw_rules"], chainsaw_outputh_path, selected_evtx_files)
        logger.info("Executing Chainsaw command {}".format(chainsaw_comand))
        print(colored("Executing Chainsaw command {}".format(chainsaw_comand), "cyan"))
        os.system(chainsaw_comand)

        output_chainsaw = glob.glob("{}/*.csv".format(chainsaw_outputh_path))
        if len(output_chainsaw) > 0:
            for el in output_chainsaw:
                logger.warning("Found suspicious activity with Chainsaw in {}".format(el))
                print(colored("Found suspicious activity with Chainsaw in {}".format(el), "red"))

def monitornewfolder(config, folder):
    logger.info("Monitor folder {} for new files".format(folder))
    try:
        f = open(config["import_state_file"], "r")
        previous_state = float(f.read())
        f.close()
    except:
        logger.info("Reset state to 0")
        previous_state = 0.0

    dirs_in_folder = glob.glob("{}/*".format(folder))
    for asset in dirs_in_folder:
        if os.path.isdir(asset):
            mtime = os.path.getmtime(asset)
            if mtime > previous_state:
                processfolder(config, asset)

    current_state = time.time()        
    f = open(config["import_state_file"], "w")
    f.write(str(current_state))
    f.close()

def monitornew(config, folder):
    logger.info("Monitor folder {} for new ZIP files".format(folder))    
    try:
        f = open(config["import_state_file"], "r")
        previous_state = float(f.read())
        f.close()
    except:
        logger.info("Reset state to 0")
        previous_state = 0.0

    dirs_in_folder = glob.glob("{}/*.zip".format(folder))
    for asset in dirs_in_folder:
        mtime = os.path.getmtime(asset)
        if mtime > previous_state:
            process(config, asset)

    current_state = time.time()        
    f = open(config["import_state_file"], "w")
    f.write(str(current_state))
    f.close()

def monitornewevtx(config, folder):
    logger.info("Monitor folder {} for new ZIP files with Windows lgos".format(folder))    
    try:
        f = open(config["import_state_file"], "r")
        previous_state = float(f.read())
        f.close()
    except:
        logger.info("Reset state to 0")
        previous_state = 0.0

    dirs_in_folder = glob.glob("{}/*.zip".format(folder))
    for asset in dirs_in_folder:
        mtime = os.path.getmtime(asset)
        if mtime > previous_state:
            processevtx(config, asset)
    
    current_state = time.time()        
    f = open(config["import_state_file"], "w")
    f.write(str(current_state))
    f.close()


def processfolder(config, folder):
    logger.info("Process folder {}".format(folder))
    full_output_path = folder
    if full_output_path:
        logger.info("Process Windows logs")
        process_windows_logs(full_output_path, config.get("always_import", True))

        logger.info("Process screening files")
        process_audit_files(full_output_path)

        if config["execute_chainsaw"]:
            logger.info("Process chainsaw")
            process_chainsaw(full_output_path)

def processevtx(config, zipfile):
    logger.info("Process ZIP {} with EVTX".format(zipfile))
    full_output_path = extract_zip(zipfile)
    if full_output_path:
        logger.info("Process Windows logs")        
        process_windows_logs(full_output_path, config.get("always_import", False), config.get("processevtx_logfolder", False))
        
        if config.get("always_delete_outputfiles", False):
            if config.get("processevtx_logfolder", False):
                # Remove everything after /output, use it first as a separator
                full_output_path = "{}/output".format(full_output_path.split("/output")[0])
                rm_remove_files = "rm -rf {}/{}".format(full_output_path, config.get("processevtx_logfolder"))
            else:
                rm_remove_files = "rm -rf {}".format(full_output_path)
            os.system(rm_remove_files)
            logger.warning("Delete {}".format(rm_remove_files))
        elif not config.get("keep_output_files", False):
            answer = input("Remove the extracted files from disk? This will not remove the information from Elastic. Answer 'yes' or leave blank to keep the files. ")
            if answer.lower() == "yes":
                if config.get("processevtx_logfolder", False):
                    # Remove everything after /output, use it first as a separator
                    full_output_path = "{}/output".format(full_output_path.split("/output")[0])
                    rm_remove_files = "rm -rf {}/{}".format(full_output_path, config.get("processevtx_logfolder"))
                else:
                    rm_remove_files = "rm -rf {}".format(full_output_path)
                os.system(rm_remove_files)
                logger.warning("Delete {}".format(rm_remove_files))
                print(colored("Delete {}".format(rm_remove_files), "red"))

def process(config, zipfile):
    logger.info("Process ZIP {}".format(zipfile))
    full_output_path = extract_zip(zipfile)
    if full_output_path:
        logger.info("Process Windows logs")
        process_windows_logs(full_output_path, config.get("always_import", False))

        logger.info("Process screening files")
        process_audit_files(full_output_path)

        if config["execute_chainsaw"]:
            logger.info("Process chainsaw")
            process_chainsaw(full_output_path)

        if config.get("always_delete_outputfiles", False):
            rm_remove_files = "rm -rf {}".format(full_output_path)
            os.system(rm_remove_files)
            logger.warning("Delete {}".format(rm_remove_files))
        elif not config.get("keep_output_files", False):
            answer = input("Remove the extracted files from disk? This will not remove the information from Elastic. Answer 'yes' or leave blank to keep the files. ")
            if answer.lower() == "yes":
                rm_remove_files = "rm -rf {}".format(full_output_path)
                os.system(rm_remove_files)
                logger.warning("Delete {}".format(full_output_path))
                print(colored("Delete {}".format(full_output_path), "red"))


def deletescreening(config, hostname):
    if len(hostname) > 0:
        query = {"bool": {"must": [], "filter": [{"match_phrase": {
                "hostname": hostname
            }}], "should": [], "must_not": []}}
        result = elasticsearch.delete_by_query(index="screening-results-*", query=query)
        logger.info("Deleted {}".format(result))
        print(result)
    else:
        print("No valid hostname supplied")


def deletescreeninglogs(config, hostname):
    if len(hostname) > 0:
        query = {"bool": {"must": [], "filter": [{"match_phrase": {
                "winlog.computer_name": hostname
            }}], "should": [], "must_not": []}}
        result = elasticsearch.delete_by_query(index="so-beats-*", query=query)
        logger.info("Deleted {}".format(result))
        print(result)
    else:
        print("No valid hostname supplied")


def listscreening(config):
    query = {
    "bool": {
      "must": [],
      "filter": [],
      "should": [],
      "must_not": []
       }
    }

    hostnames = []
    result = elasticsearch.search(index="screening-results-*", query=query, source="hostname", size=config["elasticsearch_max_results"])
    if "hits" in result and "total" in result["hits"]:
        for hostname in result["hits"]["hits"]:
            if hostname["_source"]["hostname"] not in hostnames:
                hostnames.append(hostname["_source"]["hostname"])

    print("There are {} hostnames in security screening data. \n".format(len(hostnames)))
    for el in hostnames:
        print(el)


def listscreeninglogs(config):
    query = {
    "bool": {
      "must": [],
      "filter": [
        {
          "range": {
            "@timestamp": {
              "format": "strict_date_optional_time",
              "gte": "2021-01-01T00:00:00.00Z"
            }
          }
        },
        {
          "match_phrase": {
            "event.module": "windows_eventlog"
          }
        }
      ],
      "should": [],
      "must_not": []
    }
        }

    aggregations = {"winlog.computer_name": {"terms": {"field": "winlog.computer_name"}}}
    result = elasticsearch.search(index="so-beats-*", query=query, aggregations=aggregations, source="winlog.computer_name", size=10000)
    computer_names = []
    if "hits" in result and "total" in result["hits"]:
        for computer_name in result["hits"]["hits"]:
            if computer_name["_source"]["winlog"]["computer_name"] not in computer_names:
                computer_names.append(computer_name["_source"]["winlog"]["computer_name"])

    print("There are {} FQDNs in security screening data logs. \n".format(len(computer_names)))
    for el in computer_names:
        print(el)


def report(config, zipfile):

    logger.info("Process ZIP")
    full_output_path = extract_zip(zipfile)
    if full_output_path:
        logger.info("Process screening files")

        logger.info("Audit files: system info for {}".format(full_output_path))
        print(colored("Audit files: system info for {}".format(full_output_path)))
        audit_hostname = screening_system_name(config, False, full_output_path)

        logger.info("Audit files: software list for {}".format(audit_hostname))
        software_list(config, False, full_output_path, audit_hostname)

        logger.info("Audit files: listening services for {}".format(audit_hostname))
        listening_services(config, False, full_output_path, audit_hostname)

        logger.info("Audit files: user accounts for {}".format(audit_hostname))
        user_accounts(config, False, full_output_path, audit_hostname)

        logger.info("Audit files: AV for {}".format(audit_hostname))
        anti_virus(config, False, full_output_path, audit_hostname)

def deletematchinglogs(config, evtx_file_path):
    first_timestamp = False
    last_timestamp = False
    computer_list = []
    channel = ""
    record_counter = 0

    try:
        logger.info("Reading EVTX file {}".format(evtx_file_path))
        with evtx.Evtx(evtx_file_path) as log:
            record = next(log.records())
            first_timestamp = record.timestamp().isoformat()
            last_timestamp = first_timestamp
            for record in log.records():
                computer = record.xml().split("<Computer>")[1].split("</Computer")[0]
                if computer not in computer_list:
                    computer_list.append(computer)
                channel = record.xml().split("<Channel>")[1].split("</Channel")[0]
                timestamp = record.timestamp().isoformat()
                if timestamp < first_timestamp:
                    first_timestamp = timestamp
                elif timestamp > last_timestamp:
                    last_timestamp = timestamp
            
                record_counter += 1
                if record_counter % 500 == 0:
                    logger.info("  Read {} records".format(record_counter))

        logger.info(" Received {} records, first timestamp: {}, last timestamp: {}, computer list: {}, channel: {}".format(record_counter, first_timestamp, last_timestamp, computer_list, channel))

        for computer in computer_list:            
            query = {"bool": {"must": [], "filter": [{
                        "bool": {
                            "filter": [
                            {"bool": {"should": [{"match_phrase": {"winlog.channel": channel}}],"minimum_should_match": 1}},
                            {"bool": {"should": [{"match_phrase": {"winlog.computer_name": computer}}],"minimum_should_match": 1}},
                            {"bool": {"should": [{"range": {"@timestamp": {"gte": "{}Z".format(first_timestamp),
                                                                           "lte": "{}Z".format(last_timestamp),"time_zone": "Europe/Brussels"}}}],
                                                    "minimum_should_match": 1}}]}
                        }], "should": [], "must_not": []}}            
            result = elasticsearch.delete_by_query(index="so-beats-*", query=query)
            logger.info(" Deleted records for {}: {}".format(computer, result))

    except Exception as e:
        print(f"Error for deletematchinglogs : {e}")
        logger.info("Error for deletematchinglogs : {e}")

    logger.info("Finished processing {}".format(evtx_file_path))

def create_es(config):
    logger.warning("Recreated Elasticsearch index")
    elasticsearch.indices.create(index=config["elasticsearch_index"], mappings=screening_mapping)


if __name__ == '__main__':
    from config import config

    logger = logging.getLogger("security-screening")
    logger.setLevel(logging.DEBUG)
    ch = logging.FileHandler(config["logfile"], mode="a")
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if os.stat(config["logfile"]).st_size > config["logfile_maxsize"]:
        with open(config["logfile"], 'rb') as f_in:
            with gzip.open("{}.gz".format(config["logfile"]), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        f = open(config["logfile"], "w")
        f.close()
        logger.info("Truncated logfile. Stored in {}.gz".format(config["logfile"]))

    elasticsearch = Elasticsearch(config["elasticsearch_host"], api_key=config["elasticsearch_api_key"], verify_certs=config["elasticsearch_verify_certs"], ssl_show_warn=False)

    parser = argparse.ArgumentParser(description="Process security screening data.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--process", dest="process", action="store_const", const="process", help="Import one ZIP file. Requires the location of the ZIP file.")
    parser.add_argument("--processevtx", dest="processevtx", action="store_const", const="processevtx", help="Import one ZIP file with EVTX files.")
    parser.add_argument("--processfolder", dest="processfolder", action="store_const", const="processfolder", help="Import extracted data from a specific folder. Requires the folder location.")
    parser.add_argument("--monitornew", dest="monitornew", action="store_const", const="monitornew", help="Monitor a specific folder for new ZIPs and then import them. Same as 'process' but for all ZIPs in a folder.")
    parser.add_argument("--monitornewevtx", dest="monitornewevtx", action="store_const", const="monitornewevtx", help="Monitor a specific folder for new ZIPs with only Windows log files and then import them. Same as 'process' but for all ZIPs in a folder.")    
    parser.add_argument("--monitornewfolder", dest="monitornewfolder", action="store_const", const="monitornewfolder", help="Monitor specific path for new screening data and import the data. Same as 'processfolder' but for all folders containing extracted data.")
    parser.add_argument("--listscreening", dest="listscreening", action="store_const", const="listscreening", help="List security screening data hostnames.")
    parser.add_argument("--listscreeninglogs", dest="listscreeninglogs", action="store_const", const="listscreeninglogs", help="List security screening logs FQDNs.")
    parser.add_argument("--deletescreening", dest="deletescreening", action="store_const", const="deletescreening", help="Delete screening data from Elastic. Requires hostname.")
    parser.add_argument("--deletescreeninglogs", dest="deletescreeninglogs", action="store_const", const="deletescreeninglogs", help="Delete log files from Elastic data. Requires FQDN (from winlog.computer_name).")
    parser.add_argument("--report", dest="report", action="store_const", const="report", help="Create a report")
    parser.add_argument("--createes", dest="createes", action="store_const", const="createes", help="Create Elastic index for security screening")
    parser.add_argument("--deletematchinglogs", dest="deletematchinglogs", action="store_const", const="Provide an EVTX file and delete matching records from Elastic", help="")    

    parser.add_argument("ZIP_or_hostname_or_FQDN", metavar="A ZIP file, short hostname or FQDN", type=str, help="ZIP, hostname or FQDN")
    args = parser.parse_args()

    if args.process == "process":
        logger.info("Start processing import")
        process(config, args.ZIP_or_hostname_or_FQDN)
        logger.info("End processing import")
    elif args.processevtx == "processevtx":
        logger.info("Start processevtx")
        processevtx(config, args.ZIP_or_hostname_or_FQDN)
        logger.info("End processevtxt")
    elif args.processfolder == "processfolder":
        logger.info("Start processing folder")
        processfolder(config, args.ZIP_or_hostname_or_FQDN)
        logger.info("End processing folder")
    elif args.monitornew == "monitornew":
        logger.info("Start monitornew")        
        monitornew(config, args.ZIP_or_hostname_or_FQDN)
        logger.info("End monitornew")        
    elif args.monitornewfolder == "monitornewfolder":
        logger.info("Start monitornewfolder")        
        monitornewfolder(config, args.ZIP_or_hostname_or_FQDN)     
        logger.info("End monitornewfolder")   
    elif args.monitornewevtx == "monitornewevtx":
        logger.info("Start monitornewevtx")        
        monitornewevtx(config, args.ZIP_or_hostname_or_FQDN)     
        logger.info("End monitornewevtx")           
    elif args.listscreening == "listscreening":
        logger.info("Start listscreening")
        listscreening(config)
        logger.info("End listscreening")
    elif args.listscreeninglogs == "listscreeninglogs":
        logger.info("Start listscreeninglogs")
        listscreeninglogs(config)
        logger.info("End listscreeninglogs")
    elif args.deletescreening == "deletescreening":
        logger.info("Start deletescreening")
        deletescreening(config, args.ZIP_or_hostname_or_FQDN)
        logger.info("End deletescreening")
    elif args.deletescreeninglogs == "deletescreeninglogs":
        logger.info("Start deletescreeninglogs")
        deletescreeninglogs(config, args.ZIP_or_hostname_or_FQDN)
        logger.info("End deletescreeninglogs")
    elif args.report == "report":
        logger.info("Start screening report")
        report(config, args.ZIP_or_hostname_or_FQDN)
        logger.info("End screening report")        
    elif args.createes == "createes":
        logger.info("Create Elasticsearch index")
        create_es(config)
    elif args.deletematchinglogs == "deletematchinglogs":
        logger.info("Start deletematchinglogs")
        deletematchinglogs(config, args.ZIP_or_hostname_or_FQDN)
        logger.info("End deletematchinglogs")        
