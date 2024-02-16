import pandas as pd
import io
import sys
import json
import os
from datetime import datetime
import urllib, base64
from jinja2 import Environment, FileSystemLoader
from elasticsearch import Elasticsearch
from weasyprint import HTML, CSS
import matplotlib.pyplot as plt
import logging
from config import config
from report_queries import report_queries
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# https://files.pythonhosted.org/packages/9c/3d/a121f284241f08268b21359bd425f7d4825cffc5ac5cd0e1b3d82ffd2b10/pytz-2024.1-py2.py3-none-any.whl
# https://rpmfind.net/linux/centos/7.9.2009/os/x86_64/Packages/libjpeg-turbo-devel-1.2.90-8.el7.x86_64.rpm
#  python -m pip install WeasyPrint==52.5
#export LC_CTYPE="en_US.UTF-8"


def report_screening_number_hosts(elasticsearch):
    result = elasticsearch.search(index="screening-results-*", query=report_queries["report_screening_number_hosts"]["query"], aggs=report_queries["report_screening_number_hosts"]["aggs"], size=0)
    buckets = result.get("aggregations", []).get("0", [])
    return buckets.get("value", 0)


def report_generic_aggregate(elasticsearch, query, source_field, column1, column2, create_graph=False, value_bucket=False):
    result = elasticsearch.search(index="screening-results-*", query=report_queries[query]["query"], aggs=report_queries[query]["aggs"], fields=report_queries[query]["fields"], source=source_field, size=config["elasticsearch_max_results"])
    buckets = result.get("aggregations", []).get("0", []).get("buckets", [])
    sum_other_doc_count = result.get("aggregations", []).get("0", []).get("sum_other_doc_count", 0)
    entries = {}
    for entry in buckets:
        key = entry["key"]
        if not value_bucket:
            value = entry["doc_count"]
        else:
            value = entry["1"]["buckets"][0]["key"].strip()
        if isinstance(value, int) or len(value) > 0:
            entries[key] = value
    if sum_other_doc_count > 0:
        entries["Other"] = sum_other_doc_count
    if len(entries) > 0:
        df = pd.DataFrame(list(entries.items()), columns=[column1, column2])

        if create_graph:
            labels = entries.keys()
            sizes = entries.values()
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', wedgeprops={"linewidth": 1.0, "edgecolor": "white"}, textprops={"size": "smaller"})
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = 'data:image/png;base64,' + urllib.parse.quote(string)
            chart = '<img src = "%s" />' % uri
        else:
            chart = '<img src="blank.png">'
    else:
        df = pd.DataFrame(list(["No results"]))
        chart = '<img src="blank.png">'

    df.style.hide_index()
    df.style.set_properties(**{'text-align': 'left'})

    return df, chart


def report_generic_table_details(elasticsearch, query, field1, field2, column1, column2):
    result = elasticsearch.search(index="screening-results-*", query=report_queries[query]["query"], size=config["elasticsearch_max_results"])
    entries = {}
    if "hits" in result and "total" in result["hits"]:
        for entry in result["hits"]["hits"]:
            field1_value = entry["_source"][field1]
            field2_value = entry["_source"][field2]
            if len(field1_value) > 0 and len(field2_value) > 0:
                if entries.get(field1_value, False):
                    if field2_value not in entries[field1_value]:
                        entries[field1_value].append(field2_value)
                else:
                    entries[field1_value] = [field2_value]
        entries_clean = {}
        for entry in entries:
            entries_clean[entry] = " ; ".join(entries[entry])
    if len(entries_clean) > 0:
        df = pd.DataFrame(list(entries_clean.items()), columns=[column1, column2])
    else:
        df = pd.DataFrame(list(["No results"]))
    return df


def monitoring_generic(elasticsearch, query, current_date, custom_size, field1, field1_col, field2, field2_col, event_data_field1, event_data_field1_col, event_data_field2, event_data_field2_col, user_data_field1, user_data_field1_col, event_data_field3=False, event_data_field3_col=False):
    query_replace = json.loads(json.dumps(report_queries[query]["query"]).replace("LTE_KEY_VALUE", "{}T23:59:59".format(current_date)))
    result = elasticsearch.search(index="so-beats-*", query=query_replace, size=custom_size)
    entries = []
    if "hits" in result and "total" in result["hits"]:
        for entry in result["hits"]["hits"]:
            if "@timestamp" in entry["_source"]:
                timestamp = entry["_source"]["@timestamp"]
                entry_winlog = entry["_source"].get("winlog", False)
                if entry_winlog:
                    field1_data = entry_winlog[field1]
                    field2_data = entry_winlog[field2]
                    event_data_field1_data = entry_winlog["event_data"].get(event_data_field1, "")
                    event_data_field2_data = entry_winlog["event_data"].get(event_data_field2, "")
                    user_data_field1_data = ""
                    if event_data_field3:
                        event_data_field3_data = entry_winlog["event_data"].get(event_data_field3, "")
                        entries.append({"timestamp": timestamp,
                                    field1_col: field1_data,
                                    field2_col: field2_data,
                                    event_data_field1_col: event_data_field1_data,
                                    event_data_field2_col: event_data_field2_data,
                                    event_data_field3_col: event_data_field3_data
                                    })
                    elif "user" in entry_winlog:
                        user_data_field1_data = entry_winlog["user"].get(user_data_field1, "")
                        entries.append({"timestamp": timestamp,
                                    field1_col: field1_data,
                                    field2_col: field2_data,
                                    event_data_field1_col: event_data_field1_data,
                                    event_data_field2_col: event_data_field2_data
                                    })                        
                    else:
                        entries.append({"timestamp": timestamp,
                                    field1_col: field1_data,
                                    field2_col: field2_data,
                                    event_data_field1_col: event_data_field1_data,
                                    event_data_field2_col: event_data_field2_data,
                                    user_data_field1_col: user_data_field1_data
                                    })
    if len(entries) > 0:
        df = pd.DataFrame.from_dict(entries)
    else:
        df = pd.DataFrame(list(["No results"]))
    return df


def monitoring_generic_table_details(elasticsearch, query, size, source_field, column1, column2, value_bucket=False):
    query_replace = json.loads(json.dumps(report_queries[query]["query"]).replace("LTE_KEY_VALUE", "{}T23:59:59".format(current_date)))
    result = elasticsearch.search(index="so-beats-*", query=query_replace, aggs=report_queries[query]["aggs"], fields=report_queries[query]["fields"], source=source_field, size=size)
    buckets = result.get("aggregations", []).get("0", []).get("buckets", [])
    sum_other_doc_count = result.get("aggregations", []).get("0", []).get("sum_other_doc_count", 0)
    entries = {}
    for entry in buckets:
        key = entry["key"]
        if not value_bucket:
            value = entry["doc_count"]
        else:
            value = entry["1"]["buckets"][0]["key"].strip()
        if isinstance(value, int) or len(value) > 0:
            entries[key] = value
    if sum_other_doc_count > 0:
        entries["Other"] = sum_other_doc_count
    if len(entries) > 0:
        df = pd.DataFrame(list(entries.items()), columns=[column1, column2])
    else:
        df = pd.DataFrame(list(["No results"]))

    df.style.hide_index()
    df.style.set_properties(**{'text-align': 'left'})
    return df


def send_email(sender_email, sender_password, receiver_email, subject, body, file_path, reporting_smtp_server, reporting_smtp_port):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Open PDF file in binary mode
    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file_path}",
    )

    message.attach(part)
    text = message.as_string()

    with smtplib.SMTP(reporting_smtp_server, reporting_smtp_port) as server:
        #server.starttls()
        #server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, text)


if __name__ == '__main__':
    logger = logging.getLogger("security-screening")
    logger.setLevel(logging.DEBUG)
    ch = logging.FileHandler(config["logfile"], mode="a")
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    elasticsearch = Elasticsearch(config["elasticsearch_host"], api_key=config["elasticsearch_api_key"], verify_certs=config["elasticsearch_verify_certs"], ssl_show_warn=False)
    current_date = datetime.now().strftime("%Y-%m-%d")

    monitoring_new_services = monitoring_generic(elasticsearch, "report_monitoring_new_services", current_date, 100, "computer_name", "Computer", "event_id", "Event ID", "ServiceAccount", "ServiceAccount", "ServiceFileName", "ServiceFileName", "name", "Username", "ServiceName", "ServiceName")
    monitoring_rare_scheduled_tasks = monitoring_generic_table_details(elasticsearch, "report_monitoring_rare_scheduled_tasks", 100, "winlog.event_data.ActionName.keyword", "Scheduled task action data", "Count")
    monitoring_rare_powershell = monitoring_generic_table_details(elasticsearch, "report_monitoring_rare_powershell", 100, "winlog.event_data.Path", "Powershell script", "Count")
    monitoring_logins = monitoring_generic(elasticsearch, "report_monitoring_logins", current_date, 50, "computer_name", "Computer", "event_id", "Event ID", "TargetUserName", "Target user", "IpAddress", "IP", "name", "Username")
    monitoring_logins_rdp = monitoring_generic(elasticsearch, "monitoring_logins_rdp", current_date, 50, "computer_name", "Computer", "event_id", "Event ID", "TargetUserName", "Target user", "IpAddress", "IP", "name", "Username")
    monitoring_failed_logins = monitoring_generic(elasticsearch, "report_monitoring_failed_logins", current_date, 100, "computer_name", "Computer", "event_id", "Event ID", "TargetUserName", "Target user", "IpAddress", "IP", "name", "Username")
    monitoring_new_users = monitoring_generic(elasticsearch, "report_monitoring_new_users", current_date, 50, "computer_name", "Computer", "event_id", "Event ID", "TargetUserName", "Target user", "IpAddress", "IP", "name", "Username")
    monitoring_account_locked = monitoring_generic(elasticsearch, "report_monitoring_account_locked", current_date, 50, "computer_name", "Computer", "event_id", "Event ID", "TargetUserName", "Target user", "IpAddress", "IP", "name", "Username")
    monitoring_local_group_membership_change = monitoring_generic(elasticsearch, "report_monitoring_local_group_membership_change", current_date, 50, "computer_name", "Computer", "event_id", "Event ID", "TargetUserName", "Target user", "IpAddress", "IP", "name", "Username")
    monitoring_password_reset_attempt = monitoring_generic(elasticsearch, "report_monitoring_password_reset_attempt", current_date, 50, "computer_name", "Computer", "event_id", "Event ID", "TargetUserName", "Target user", "IpAddress", "IP", "name", "Username")

    holder = False
    screening_os_table_details, holder = report_generic_aggregate(elasticsearch, "report_screening_os_table_details", "os_name.keyword", "Hostname", "Operating system", False, True)
    screening_os_table, screening_os_table_chart = report_generic_aggregate(elasticsearch, "report_screening_os", "os_name.keyword", "Operating system", "Count", True, False)

    screening_software_table_details_rare, screening_software_table_details_rare_chart = report_generic_aggregate(elasticsearch, "report_screening_software_table_details_rare", "software.keyword", "Software", "Count", True, False)
    screening_software_table_details = report_generic_table_details(elasticsearch, "report_screening_software_table_details", "hostname", "software", "Software", "Count")
    screening_software, screening_software_chart = report_generic_aggregate(elasticsearch, "report_screening_software", "software.keyword", "Software", "Count", True, False)
    screening_number_hosts = report_screening_number_hosts(elasticsearch)
    screening_av_status_details, screening_av_status_details_chart = report_generic_aggregate(elasticsearch, "report_screening_av_status", "anti_malware.keyword", "Software", "Count", True, False)
    screening_active_users, screening_active_users_chart = report_generic_aggregate(elasticsearch, "report_screening_active_users", "active.keyword", "Status", "Count", True, False)
    screening_expiration_date_users, screening_expiration_date_users_chart = report_generic_aggregate(elasticsearch, "report_screening_users_expiration_date", "expires.keyword", "Expiration date", "Count", True, False)
    screening_last_logon_date_users, screening_last_logon_date_users_chart = report_generic_aggregate(elasticsearch, "report_screening_users_lastlogon", "last_logon.keyword", "Last logon", "Count", True, False)
    screening_users_table_details = report_generic_table_details(elasticsearch, "report_screening_users_table_details", "hostname", "username", "Hostname", "Username")

    env = Environment(loader=FileSystemLoader(""))
    template = env.get_template("reporting_template.html")
    html = template.render(report_title="Security Onion report",
                        report_date=current_date,
                        monitoring_rare_scheduled_tasks=monitoring_rare_scheduled_tasks,
                        monitoring_rare_powershell=monitoring_rare_powershell,
                        monitoring_new_services=monitoring_new_services,
                        monitoring_logins=monitoring_logins,
                        monitoring_logins_rdp=monitoring_logins_rdp,
                        monitoring_failed_logins=monitoring_failed_logins,
                        monitoring_new_users=monitoring_new_users,
                        monitoring_password_reset_attempt=monitoring_password_reset_attempt,
                        monitoring_local_group_membership_change=monitoring_local_group_membership_change,
                        monitoring_account_locked=monitoring_account_locked,
                        screening_users_table_details=screening_users_table_details,
                        screening_last_logon_date_users=screening_last_logon_date_users,
                        screening_expiration_date_users=screening_expiration_date_users,
                        screening_expiration_date_users_chart=screening_expiration_date_users_chart,
                        screening_active_users=screening_active_users,
                        screening_last_logon_date_users_chart=screening_last_logon_date_users_chart,
                        screening_active_users_chart=screening_active_users_chart,
                        screening_av_status_details_chart=screening_av_status_details_chart,
                        screening_av_status_details=screening_av_status_details,
                        screening_number_hosts=screening_number_hosts,
                        screening_software=screening_software,
                        screening_software_table_details=screening_software_table_details,
                        screening_software_table_details_rare=screening_software_table_details_rare,
                        screening_os_table_details=screening_os_table_details,
                        screening_os_table_chart=screening_os_table_chart
                        )
    with open("reporting-report-{}.html".format(current_date), "w") as f:
        f.write(html)

    css = CSS(string='''
        @page {size: A4; margin: 1cm;}
        ''')
    HTML("reporting-report-{}.html".format(current_date)).write_pdf("reporting-report-{}.pdf".format(current_date), stylesheets=[css])

    subject = "Security Onion reporting - {}".format(current_date)
    body = "Please find attached the PDF file."
    file_path = "reporting-report-{}.pdf".format(current_date)
    send_email(config["reporting_sender"], "", config["reporting_receiver"], subject, body, file_path, config["reporting_smtp_server"], config["reporting_smtp_port"])
    os.remove(file_path)
    os.remove("reporting-report-{}.html".format(current_date))