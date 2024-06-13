import csv
from datetime import datetime, timedelta

def parse_csvde_output(file_path):
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        # Print column names (Optional, to understand what data is available)
        print("Columns in the file:", reader.fieldnames)
        
        # Process each row in the CSV file
        for row in reader:
            dn = row.get("distinguishedName", "")
            cn = row.get("cn", "")  
            objectClass = row.get("objectClass", "")
            memberOf = row.get("memberOf", "")
            whenCreated = row.get("whenCreated", False)
            lastLogon = row.get("lastLogon", False)
            human_whenCreated = ""
            human_lastLogon = ""
            if whenCreated:
                dt_obj = datetime.strptime(whenCreated, "%Y%m%d%H%M%S.0Z")
                human_whenCreated = dt_obj.strftime("%Y-%m-%d %H:%M:%S UTC")
            if lastLogon:
                last_logon_int = int(lastLogon)
                human_lastLogon = datetime(1601, 1, 1) + timedelta(microseconds=last_logon_int // 10)
                human_lastLogon = human_lastLogon.strftime("%Y-%m-%d %H:%M:%S UTC")

            if objectClass == "computer": #"user"
                print(f"{cn}|{human_whenCreated}|{human_lastLogon}|{memberOf}")

file_path = "adquery_users.csv"
parse_csvde_output(file_path)

