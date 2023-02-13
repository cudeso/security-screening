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

from elasticsearch import Elasticsearch
from screening_mapping import screening_mapping
from screening_helpers import *

from screening_data import *

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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


def process_windows_logs(full_output_path):
    for el in config["evtx_logs_to_process"]:
        evtx_file = "{}/logs/{}".format(full_output_path, el)
        if os.path.isfile(evtx_file):
            logger.info("Processing {}".format(evtx_file))
            with open(evtx_file, "rb") as f:
                data = f.read()
                md5hash = hashlib.md5(data).hexdigest()
                full_path_existing_log = "{}{}".format(config["nsm_evtx"], md5hash)
            import_file = True
            if os.path.exists(full_path_existing_log):
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


def process(config, zipfile):

    logger.info("Process ZIP")
    full_output_path = extract_zip(zipfile)
    if full_output_path:
        logger.info("Process Windows logs")
        process_windows_logs(full_output_path)

        logger.info("Process screening files")
        process_audit_files(full_output_path)

        if config["execute_chainsaw"]:
            logger.info("Process chainsaw")
            process_chainsaw(full_output_path)

        answer = input("Remove the extracted files from disk? This will not remove the information from Elastic. Answer 'yes' or leave blank to keep the files. ")
        if answer.lower() == "yes":
            rm_remove_files = "rm -rf {}".format(full_output_path)
            os.system(rm_remove_files)
            logger.warning("Delete {}".format(full_output_path))
            print(colored("Delete {}".format(full_output_path), "red"))


def delete_screening(config, hostname):
    if len(hostname) > 0:
        query = {"bool": {"must": [], "filter": [{"match_phrase": {
                "hostname": hostname
            }}], "should": [], "must_not": []}}
        result = elasticsearch.delete_by_query(index="screening-results-*", query=query)
        logger.info("Deleted {}".format(result))
        print(result)
    else:
        print("No valid hostname supplied")


def delete_logs(config, hostname):
    if len(hostname) > 0:
        query = {"bool": {"must": [], "filter": [{"match_phrase": {
                "winlog.computer_name": hostname
            }}], "should": [], "must_not": []}}
        result = elasticsearch.delete_by_query(index="so-beats-*", query=query)
        logger.info("Deleted {}".format(result))
        print(result)
    else:
        print("No valid hostname supplied")


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
    parser.add_argument("--process", dest="process", action="store_const", const="process", help="Import a ZIP. Requires the location of the ZIP file.")
    parser.add_argument("--deletescreening", dest="deletescreening", action="store_const", const="deletescreening", help="Delete screening data stored in Elasticsearch. Requires simple hostname.")
    parser.add_argument("--deletelogs", dest="deletelogs", action="store_const", const="deletelogs", help="Delete screening data stored in Elasticsearch. Requires FQDN name (from winlog.computer_name).")
    parser.add_argument("ZIP_or_hostname_or_FQDN", metavar="A ZIP file, short hostname or FQDN", type=str, help="ZIP, hostname or FQDN")
    args = parser.parse_args()

    if args.process == "process":
        logger.info("Start processing import")
        process(config, args.ZIP_or_hostname_or_FQDN)
        logger.info("End processing import")
    elif args.deletescreening == "deletescreening":
        logger.info("Start screening delete")
        delete_screening(config, args.ZIP_or_hostname_or_FQDN)
        logger.info("End screening delete")
    elif args.deletelogs == "deletelogs":
        logger.info("Start log delete")
        delete_logs(config, args.ZIP_or_hostname_or_FQDN)
        logger.info("End log delete")
    elif args.createes == "createes":
        logger.info("Create Elasticsearch index")
        create_es(config)
