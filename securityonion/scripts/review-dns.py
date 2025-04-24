import os
import re

'''
Parse Windows DNS log files
Koen Van Impe
'''
query_regex = re.compile(
    r"(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}) .*? PACKET .*? Rcv ([\d\.]+).*? Q .*? A\s+(.*)"
)

def decode_domain_name(encoded_domain):
    """
    Decodes a DNS-encoded domain name by removing length prefixes and trailing '0'.
    Example: '(8)umwatson(6)events(4)data(9)microsoft(3)com(0)' -> 'umwatson.events.data.microsoft.com'
    """
    segments = re.split(r"\(\d+\)", encoded_domain)
    decoded = ".".join(filter(None, segments))
    return decoded.strip(".0").lower()

def get_tld_and_domain(domain):
    parts = domain.split(".")
    if len(parts) > 1:
        return ".".join(parts[-2:]).lower()
    return domain.lower()

def cleanup_domain(domain):
    cleanup = ["dr nxdomain] a", "dr nxdomain] aaaa", "dr nxdomain] srv", "DR NXDOMAIN] AAAA", "DR NXDOMAIN] SRV", "DR NXDOMAIN] A"]
    for clean in cleanup:
        if clean in domain:
            domain = domain.replace(clean, "").strip()
    return domain.lower()

def extract_client_queries_from_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            match = query_regex.search(line)
            if match:
                timestamp = match.group(1)
                client_ip = match.group(2)
                raw_domain = match.group(3)

                decoded_domain = decode_domain_name(raw_domain).strip()
                tld_and_domain = get_tld_and_domain(decoded_domain).strip()

                if "NXDOMAIN" in decoded_domain or "nxdomain" in decoded_domain:
                    decoded_domain = cleanup_domain(decoded_domain)
                print(f"{timestamp}, {client_ip}, {decoded_domain}, {tld_and_domain}")

def process_all_log_files_in_directory(directory_path):
    """
    Process all files ending with .log in the specified directory.
    """
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".log"):
            file_path = os.path.join(directory_path, file_name)
            extract_client_queries_from_file(file_path)

directory_path = "/dns/"  # Replace with your directory path
process_all_log_files_in_directory(directory_path)
