screening_mapping = {
        "properties": {
            "@timestamp": { "type" : "date" },
            "hostname": {"type": "keyword"},
            "screening_type": {"type": "keyword"},
            "screening_session": {"type": "keyword"},
            "domain": {"type": "keyword"},
            "os_name": {"type": "keyword"},
            "os_version": {"type": "keyword"},
            "bios_version": {"type": "keyword"},
            "productid": {"type": "keyword"},
            "system_owner": {"type": "keyword"},
            "input_locale": {"type": "keyword"},            
            "system_locale": {"type": "keyword"},
            "timezone": {"type": "keyword"},
            "logon": {"type": "keyword"},
            "os_configuration": {"type": "keyword"},
            "os_installdate": {"type": "keyword"},
            "os_bootdate": {"type": "keyword"},
            "os_manufact": {"type": "keyword"},
            "os_model": {"type": "keyword"},
            "os_type": {"type": "keyword"},
            "cpu": {"type": "keyword"},
            "sysdir": {"type": "keyword"},
            "windir": {"type": "keyword"},
            "bootdevice": {"type": "keyword"},
            "mem_phys": {"type": "keyword"},
            "mem_virt": {"type": "keyword"},
            "hotfix": {"type": "keyword"},
            
            "username": {"type": "keyword"},
            "comment": {"type": "keyword"},
            "active": {"type": "keyword"},
            "expires": {"type": "keyword"},
            "last_logon": {"type": "keyword"},
            "local_group": {"type": "keyword"},
            "global_group": {"type": "keyword"},
            
            "software": {"type": "keyword"},
            
            "anti_malware": {"type": "keyword"},
            
            "port": {"type": "integer"},
            "pid": {"type": "integer"},
            "image_name": {"type": "keyword"},
            "session_name": {"type": "keyword"},
            "user_name": {"type": "keyword"},
            "application": {"type": "keyword"}

        },
    "properties": {
      "@timestamp": {
        "type": "date"
      }
    }
}

