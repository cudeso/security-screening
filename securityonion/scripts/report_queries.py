report_queries = {
    "report_screening_software_table_details": {
                "size": 200,
                "sort": [
                    {
                    "_score": {
                        "order": "desc"
                    }
                    }
                ],
                "fields": [
                    {
                    "field": "*",
                    "include_unmapped": "true"
                    },
                    {
                    "field": "@timestamp",
                    "format": "strict_date_optional_time"
                    },
                    {
                    "field": "timestamp",
                    "format": "strict_date_optional_time"
                    }
                ],
                "script_fields": {},
                "stored_fields": [
                    "*"
                ],
                "runtime_mappings": {},
                "query": {
                    "bool": {
                    "must": [],
                    "filter": [
                        {
                        "match_phrase": {
                            "screening_type": "software"
                        }
                        }
                    ],
                    "should": [],
                    "must_not": []
                    }
                }
                },
    "report_screening_software_table_details_rare": {
            "aggs": {
                "0": {
                "terms": {
                    "field": "software.keyword",
                    "order": {
                    "_count": "asc"
                    },
                    "size": 30
                }
                }
            },
            "size": 0,
            "fields": [
                {
                "field": "@timestamp",
                "format": "date_time"
                },
                {
                "field": "timestamp",
                "format": "date_time"
                }
            ],
            "script_fields": {},
            "stored_fields": [
                "*"
            ],
            "runtime_mappings": {},
            "_source": {
                "excludes": []
            },
            "query": {
                "bool": {
                "must": [],
                "filter": [],
                "should": [],
                "must_not": []
                }
            }
            },
    "report_screening_software": {
        "aggs": {
            "0": {
            "terms": {
                "field": "software.keyword",
                "order": {
                "_count": "desc"
                },
                "size": 20
            }
            }
        },
        "size": 0,
        "fields": [
            {
            "field": "@timestamp",
            "format": "date_time"
            },
            {
            "field": "timestamp",
            "format": "date_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "_source": {
            "excludes": []
        },
        "query": {
            "bool": {
            "must": [],
            "filter": [],
            "should": [],
            "must_not": []
            }
        }
        },
    "report_screening_os": {
        "aggs": {
            "0": {
            "terms": {
                "field": "os_name.keyword",
                "order": {
                "_count": "desc"
                },
                "size": 5
            }
            }
        },
        "size": 0,
        "fields": [
            {
            "field": "@timestamp",
            "format": "date_time"
            },
            {
            "field": "timestamp",
            "format": "date_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "_source": {
            "excludes": []
        },
        "query": {
            "bool": {
            "must": [],
            "filter": [],
            "should": [],
            "must_not": []
            }
        }
        },
    "report_screening_os_table_details": {
        "aggs": {
        "0": {
            "terms": {
            "field": "hostname.keyword",
            "order": {
                "_count": "desc"
            },
            "size": 100
            },
            "aggs": {
            "1": {
                "terms": {
                "field": "os_name.keyword",
                "order": {
                    "_count": "desc"
                },
                "size": 100
                }
            }
            }
        }
        },
        "size": 0,
        "fields": [
        {
            "field": "@timestamp",
            "format": "date_time"
        },
        {
            "field": "timestamp",
            "format": "date_time"
        }
        ],
        "script_fields": {},
        "stored_fields": [
        "*"
        ],
        "runtime_mappings": {},
        "_source": {
        "excludes": []
        },
        "query": {
        "bool": {
            "must": [],
            "filter": [],
            "should": [],
            "must_not": []
        }
        }
    },
    "report_screening_number_hosts": {
        "aggs": {
            "0": {
            "cardinality": {
                "field": "hostname.keyword"
            }
            }
        },
        "size": 0,
        "fields": [
            {
            "field": "@timestamp",
            "format": "date_time"
            },
            {
            "field": "timestamp",
            "format": "date_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "_source": {
            "excludes": []
        },
        "query": {
            "bool": {
            "must": [],
            "filter": [
                {
                "exists": {
                    "field": "hostname.keyword"
                }
                }
            ],
            "should": [],
            "must_not": []
            }
        }
        },
    "report_screening_av_status":{
        "aggs": {
            "0": {
            "terms": {
                "field": "anti_malware.keyword",
                "order": {
                "_count": "desc"
                },
                "size": 20
            }
            }
        },
        "size": 0,
        "fields": [
            {
            "field": "@timestamp",
            "format": "date_time"
            },
            {
            "field": "timestamp",
            "format": "date_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "_source": {
            "excludes": []
        },
        "query": {
            "bool": {
            "must": [],
            "filter": [],
            "should": [],
            "must_not": []
            }
        }
        },
    "report_screening_active_users": {
        "aggs": {
            "0": {
            "terms": {
                "field": "active.keyword",
                "order": {
                "_count": "desc"
                },
                "size": 5
            }
            }
        },
        "size": 0,
        "fields": [
            {
            "field": "@timestamp",
            "format": "date_time"
            },
            {
            "field": "timestamp",
            "format": "date_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "_source": {
            "excludes": []
        },
        "query": {
            "bool": {
            "must": [],
            "filter": [],
            "should": [],
            "must_not": []
            }
        }
        },
    "report_screening_users_expiration_date": {
            "aggs": {
                "0": {
                "terms": {
                    "field": "expires.keyword",
                    "order": {
                    "_count": "desc"
                    },
                    "size": 5
                }
                }
            },
            "size": 0,
            "fields": [
                {
                "field": "@timestamp",
                "format": "date_time"
                },
                {
                "field": "timestamp",
                "format": "date_time"
                }
            ],
            "script_fields": {},
            "stored_fields": [
                "*"
            ],
            "runtime_mappings": {},
            "_source": {
                "excludes": []
            },
            "query": {
                "bool": {
                "must": [],
                "filter": [],
                "should": [],
                "must_not": []
                }
            }
            },
    "report_screening_users_lastlogon": {
        "aggs": {
            "0": {
            "terms": {
                "field": "last_logon.keyword",
                "order": {
                "_count": "desc"
                },
                "size": 5
            }
            }
        },
        "size": 0,
        "fields": [
            {
            "field": "@timestamp",
            "format": "date_time"
            },
            {
            "field": "timestamp",
            "format": "date_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "_source": {
            "excludes": []
        },
        "query": {
            "bool": {
            "must": [],
            "filter": [],
            "should": [],
            "must_not": []
            }
        }
        },
    "report_screening_users_table_details": {
        "size": 200,
        "sort": [
            {
            "_score": {
                "order": "desc"
            }
            }
        ],
        "fields": [
            {
            "field": "*",
            "include_unmapped": "true"
            },
            {
            "field": "@timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "timestamp",
            "format": "strict_date_optional_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "query": {
            "bool": {
            "must": [],
            "filter": [
                {
                "match_phrase": {
                    "screening_type": "accounts"
                }
                }
            ],
            "should": [],
            "must_not": [
                {
                "match_phrase": {
                    "screening_type": "anti_malware"
                }
                }
            ]
            }
        }
        },
    "report_monitoring_logins": {
        "size": 50,
        "sort": [
            {
            "@timestamp": {
                "order": "desc",
                "unmapped_type": "boolean"
            }
            }
        ],
        "fields": [
            {
            "field": "*",
            "include_unmapped": "true"
            },
            {
            "field": "@timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "dll.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.ingested",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "package.installed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.first_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.last_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.modified_at",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.first_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.last_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.modified_at",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "winlog.time_created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.kerberos.valid.from",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.kerberos.valid.until",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.org_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.rec_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.ref_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.xmt_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.revoke.time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.update.next",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.update.this",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.pe.compile_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.changed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.modified",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smtp.date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.snmp.up_since",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.x509.certificate.valid.from",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.x509.certificate.valid.until",
            "format": "strict_date_optional_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "query": {
            "bool": {
            "must": [],
            "filter": [
                {
                "match_phrase": {
                    "winlog.event_id": "4625"
                }
                },
                {
                "range": {
                    "@timestamp": {
                    "format": "strict_date_optional_time",
                    "gte": "2023-08-06T12:09:23.724Z",
                    "lte": "LTE_KEY_VALUE"
                    }
                }
                }
            ],
            "should": [],
            "must_not": []
            }
        }
        },
    "monitoring_logins_rdp": {
        "size": 100,
        "sort": [
            {
            "@timestamp": {
                "order": "desc",
                "unmapped_type": "boolean"
            }
            }
        ],
        "fields": [
            {
            "field": "*",
            "include_unmapped": "true"
            },
            {
            "field": "@timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "dll.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.ingested",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "package.installed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.first_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.last_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.modified_at",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.first_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.last_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.modified_at",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "winlog.time_created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.kerberos.valid.from",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.kerberos.valid.until",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.org_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.rec_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.ref_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.xmt_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.revoke.time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.update.next",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.update.this",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.pe.compile_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.changed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.modified",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smtp.date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.snmp.up_since",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.x509.certificate.valid.from",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.x509.certificate.valid.until",
            "format": "strict_date_optional_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "query": {
            "bool": {
            "must": [],
            "filter": [
                {
                "match_phrase": {
                    "winlog.event_id": "4624"
                }
                },
                {
                "match_phrase": {
                    "winlog.event_data.LogonType": "10"
                }
                },
                {
                "range": {
                    "@timestamp": {
                    "format": "strict_date_optional_time",
                    "gte": "2023-08-06T12:59:42.625Z",
                    "lte": "LTE_KEY_VALUE"
                    }
                }
                }
            ],
            "should": [],
            "must_not": []
            }
        }
        },
    "report_monitoring_failed_logins": {
        "size": 100,
        "sort": [
            {
            "@timestamp": {
                "order": "desc",
                "unmapped_type": "boolean"
            }
            }
        ],
        "fields": [
            {
            "field": "*",
            "include_unmapped": "true"
            },
            {
            "field": "@timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "dll.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.ingested",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "package.installed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.first_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.last_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.modified_at",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.first_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.last_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.modified_at",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "winlog.time_created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.kerberos.valid.from",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.kerberos.valid.until",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.org_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.rec_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.ref_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.xmt_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.revoke.time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.update.next",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.update.this",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.pe.compile_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.changed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.modified",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smtp.date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.snmp.up_since",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.x509.certificate.valid.from",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.x509.certificate.valid.until",
            "format": "strict_date_optional_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "query": {
            "bool": {
            "must": [],
            "filter": [
                {
                "match_phrase": {
                    "winlog.event_id": "4625"
                }
                },
                {
                "range": {
                    "@timestamp": {
                    "format": "strict_date_optional_time",
                    "gte": "2023-08-06T13:04:47.313Z",
                    "lte": "LTE_KEY_VALUE"
                    }
                }
                }
            ],
            "should": [],
            "must_not": []
            }
        }
        },
    "report_monitoring_new_users": {
        "size": 100,
        "sort": [
            {
            "@timestamp": {
                "order": "desc",
                "unmapped_type": "boolean"
            }
            }
        ],
        "fields": [
            {
            "field": "*",
            "include_unmapped": "true"
            },
            {
            "field": "@timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "dll.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.ingested",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "package.installed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.first_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.last_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.modified_at",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.first_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.last_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.modified_at",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "winlog.time_created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.kerberos.valid.from",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.kerberos.valid.until",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.org_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.rec_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.ref_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.xmt_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.revoke.time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.update.next",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.update.this",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.pe.compile_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.changed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.modified",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smtp.date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.snmp.up_since",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.x509.certificate.valid.from",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.x509.certificate.valid.until",
            "format": "strict_date_optional_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "query": {
            "bool": {
            "must": [],
            "filter": [
                {
                "match_phrase": {
                    "winlog.event_id": "4720"
                }
                },
                {
                "range": {
                    "@timestamp": {
                    "format": "strict_date_optional_time",
                    "gte": "2023-08-06T13:08:47.949Z",
                    "lte": "LTE_KEY_VALUE"
                    }
                }
                }
            ],
            "should": [],
            "must_not": []
            }
        }
        },
    "report_monitoring_local_group_membership_change": {
        "size": 100,
        "sort": [
            {
            "@timestamp": {
                "order": "desc",
                "unmapped_type": "boolean"
            }
            }
        ],
        "fields": [
            {
            "field": "*",
            "include_unmapped": "true"
            },
            {
            "field": "@timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "dll.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.ingested",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "package.installed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.first_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.last_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.modified_at",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.first_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.last_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.modified_at",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "winlog.time_created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.kerberos.valid.from",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.kerberos.valid.until",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.org_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.rec_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.ref_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.xmt_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.revoke.time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.update.next",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.update.this",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.pe.compile_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.changed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.modified",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smtp.date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.snmp.up_since",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.x509.certificate.valid.from",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.x509.certificate.valid.until",
            "format": "strict_date_optional_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "query": {
            "bool": {
            "must": [],
            "filter": [
                {
                "match_phrase": {
                    "winlog.event_id": "4732"
                }
                },
                {
                "range": {
                    "@timestamp": {
                    "format": "strict_date_optional_time",
                    "gte": "2023-08-06T13:13:58.747Z",
                    "lte": "LTE_KEY_VALUE"
                    }
                }
                }
            ],
            "should": [],
            "must_not": []
            }
        }
        },
    "report_monitoring_account_locked": {
            "size": 100,
            "sort": [
                {
                "@timestamp": {
                    "order": "desc",
                    "unmapped_type": "boolean"
                }
                }
            ],
            "fields": [
                {
                "field": "*",
                "include_unmapped": "true"
                },
                {
                "field": "@timestamp",
                "format": "strict_date_optional_time"
                },
                {
                "field": "dll.code_signature.timestamp",
                "format": "strict_date_optional_time"
                },
                {
                "field": "event.created",
                "format": "strict_date_optional_time"
                },
                {
                "field": "event.end",
                "format": "strict_date_optional_time"
                },
                {
                "field": "event.ingested",
                "format": "strict_date_optional_time"
                },
                {
                "field": "event.start",
                "format": "strict_date_optional_time"
                },
                {
                "field": "file.accessed",
                "format": "strict_date_optional_time"
                },
                {
                "field": "file.code_signature.timestamp",
                "format": "strict_date_optional_time"
                },
                {
                "field": "file.created",
                "format": "strict_date_optional_time"
                },
                {
                "field": "file.ctime",
                "format": "strict_date_optional_time"
                },
                {
                "field": "file.elf.creation_date",
                "format": "strict_date_optional_time"
                },
                {
                "field": "file.mtime",
                "format": "strict_date_optional_time"
                },
                {
                "field": "file.x509.not_after",
                "format": "strict_date_optional_time"
                },
                {
                "field": "file.x509.not_before",
                "format": "strict_date_optional_time"
                },
                {
                "field": "package.installed",
                "format": "strict_date_optional_time"
                },
                {
                "field": "process.code_signature.timestamp",
                "format": "strict_date_optional_time"
                },
                {
                "field": "process.elf.creation_date",
                "format": "strict_date_optional_time"
                },
                {
                "field": "process.end",
                "format": "strict_date_optional_time"
                },
                {
                "field": "process.parent.code_signature.timestamp",
                "format": "strict_date_optional_time"
                },
                {
                "field": "process.parent.elf.creation_date",
                "format": "strict_date_optional_time"
                },
                {
                "field": "process.parent.end",
                "format": "strict_date_optional_time"
                },
                {
                "field": "process.parent.start",
                "format": "strict_date_optional_time"
                },
                {
                "field": "process.start",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.enrichments.indicator.file.accessed",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.enrichments.indicator.file.code_signature.timestamp",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.enrichments.indicator.file.created",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.enrichments.indicator.file.ctime",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.enrichments.indicator.file.elf.creation_date",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.enrichments.indicator.file.mtime",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.enrichments.indicator.file.x509.not_after",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.enrichments.indicator.file.x509.not_before",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.enrichments.indicator.first_seen",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.enrichments.indicator.last_seen",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.enrichments.indicator.modified_at",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.enrichments.indicator.x509.not_after",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.enrichments.indicator.x509.not_before",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.indicator.file.accessed",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.indicator.file.code_signature.timestamp",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.indicator.file.created",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.indicator.file.ctime",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.indicator.file.elf.creation_date",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.indicator.file.mtime",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.indicator.file.x509.not_after",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.indicator.file.x509.not_before",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.indicator.first_seen",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.indicator.last_seen",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.indicator.modified_at",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.indicator.x509.not_after",
                "format": "strict_date_optional_time"
                },
                {
                "field": "threat.indicator.x509.not_before",
                "format": "strict_date_optional_time"
                },
                {
                "field": "tls.client.not_after",
                "format": "strict_date_optional_time"
                },
                {
                "field": "tls.client.not_before",
                "format": "strict_date_optional_time"
                },
                {
                "field": "tls.client.x509.not_after",
                "format": "strict_date_optional_time"
                },
                {
                "field": "tls.client.x509.not_before",
                "format": "strict_date_optional_time"
                },
                {
                "field": "tls.server.not_after",
                "format": "strict_date_optional_time"
                },
                {
                "field": "tls.server.not_before",
                "format": "strict_date_optional_time"
                },
                {
                "field": "tls.server.x509.not_after",
                "format": "strict_date_optional_time"
                },
                {
                "field": "tls.server.x509.not_before",
                "format": "strict_date_optional_time"
                },
                {
                "field": "winlog.time_created",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.kerberos.valid.from",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.kerberos.valid.until",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.ntp.org_time",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.ntp.rec_time",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.ntp.ref_time",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.ntp.xmt_time",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.ocsp.revoke.time",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.ocsp.update.next",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.ocsp.update.this",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.pe.compile_time",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.smb_files.times.accessed",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.smb_files.times.changed",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.smb_files.times.created",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.smb_files.times.modified",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.smtp.date",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.snmp.up_since",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.x509.certificate.valid.from",
                "format": "strict_date_optional_time"
                },
                {
                "field": "zeek.x509.certificate.valid.until",
                "format": "strict_date_optional_time"
                }
            ],
            "script_fields": {},
            "stored_fields": [
                "*"
            ],
            "runtime_mappings": {},
            "query": {
                "bool": {
                "must": [],
                "filter": [
                    {
                    "match_phrase": {
                        "winlog.event_id": "4740"
                    }
                    },
                    {
                    "range": {
                        "@timestamp": {
                        "format": "strict_date_optional_time",
                        "gte": "2023-08-06T13:16:57.497Z",
                    "lte": "LTE_KEY_VALUE"
                        }
                    }
                    }
                ],
                "should": [],
                "must_not": []
                }
            }
            },
    "report_monitoring_password_reset_attempt": {
        "size": 100,
        "sort": [
            {
            "@timestamp": {
                "order": "desc",
                "unmapped_type": "boolean"
            }
            }
        ],
        "fields": [
            {
            "field": "*",
            "include_unmapped": "true"
            },
            {
            "field": "@timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "dll.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.ingested",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "package.installed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.first_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.last_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.modified_at",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.first_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.last_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.modified_at",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "winlog.time_created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.kerberos.valid.from",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.kerberos.valid.until",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.org_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.rec_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.ref_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.xmt_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.revoke.time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.update.next",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.update.this",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.pe.compile_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.changed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.modified",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smtp.date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.snmp.up_since",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.x509.certificate.valid.from",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.x509.certificate.valid.until",
            "format": "strict_date_optional_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "query": {
            "bool": {
            "must": [],
            "filter": [
                {
                "match_phrase": {
                    "winlog.event_id": "4724"
                }
                },
                {
                "range": {
                    "@timestamp": {
                    "format": "strict_date_optional_time",
                    "gte": "2023-08-06T13:17:38.660Z",
                    "lte": "LTE_KEY_VALUE"
                    }
                }
                }
            ],
            "should": [],
            "must_not": []
            }
        }
        },
    "report_monitoring_rare_scheduled_tasks": {
        "aggs": {
            "0": {
            "rare_terms": {
                "field": "winlog.event_data.ActionName.keyword",
                "max_doc_count": 10
            }
            }
        },
        "size": 0,
        "fields": [
            {
            "field": "@timestamp",
            "format": "date_time"
            },
            {
            "field": "dll.code_signature.timestamp",
            "format": "date_time"
            },
            {
            "field": "event.created",
            "format": "date_time"
            },
            {
            "field": "event.end",
            "format": "date_time"
            },
            {
            "field": "event.ingested",
            "format": "date_time"
            },
            {
            "field": "event.start",
            "format": "date_time"
            },
            {
            "field": "file.accessed",
            "format": "date_time"
            },
            {
            "field": "file.code_signature.timestamp",
            "format": "date_time"
            },
            {
            "field": "file.created",
            "format": "date_time"
            },
            {
            "field": "file.ctime",
            "format": "date_time"
            },
            {
            "field": "file.elf.creation_date",
            "format": "date_time"
            },
            {
            "field": "file.mtime",
            "format": "date_time"
            },
            {
            "field": "file.x509.not_after",
            "format": "date_time"
            },
            {
            "field": "file.x509.not_before",
            "format": "date_time"
            },
            {
            "field": "package.installed",
            "format": "date_time"
            },
            {
            "field": "process.code_signature.timestamp",
            "format": "date_time"
            },
            {
            "field": "process.elf.creation_date",
            "format": "date_time"
            },
            {
            "field": "process.end",
            "format": "date_time"
            },
            {
            "field": "process.parent.code_signature.timestamp",
            "format": "date_time"
            },
            {
            "field": "process.parent.elf.creation_date",
            "format": "date_time"
            },
            {
            "field": "process.parent.end",
            "format": "date_time"
            },
            {
            "field": "process.parent.start",
            "format": "date_time"
            },
            {
            "field": "process.start",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.accessed",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.code_signature.timestamp",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.created",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.ctime",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.elf.creation_date",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.mtime",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_after",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_before",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.first_seen",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.last_seen",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.modified_at",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_after",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_before",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.accessed",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.code_signature.timestamp",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.created",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.ctime",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.elf.creation_date",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.mtime",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.x509.not_after",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.x509.not_before",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.first_seen",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.last_seen",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.modified_at",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.x509.not_after",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.x509.not_before",
            "format": "date_time"
            },
            {
            "field": "tls.client.not_after",
            "format": "date_time"
            },
            {
            "field": "tls.client.not_before",
            "format": "date_time"
            },
            {
            "field": "tls.client.x509.not_after",
            "format": "date_time"
            },
            {
            "field": "tls.client.x509.not_before",
            "format": "date_time"
            },
            {
            "field": "tls.server.not_after",
            "format": "date_time"
            },
            {
            "field": "tls.server.not_before",
            "format": "date_time"
            },
            {
            "field": "tls.server.x509.not_after",
            "format": "date_time"
            },
            {
            "field": "tls.server.x509.not_before",
            "format": "date_time"
            },
            {
            "field": "winlog.time_created",
            "format": "date_time"
            },
            {
            "field": "zeek.kerberos.valid.from",
            "format": "date_time"
            },
            {
            "field": "zeek.kerberos.valid.until",
            "format": "date_time"
            },
            {
            "field": "zeek.ntp.org_time",
            "format": "date_time"
            },
            {
            "field": "zeek.ntp.rec_time",
            "format": "date_time"
            },
            {
            "field": "zeek.ntp.ref_time",
            "format": "date_time"
            },
            {
            "field": "zeek.ntp.xmt_time",
            "format": "date_time"
            },
            {
            "field": "zeek.ocsp.revoke.time",
            "format": "date_time"
            },
            {
            "field": "zeek.ocsp.update.next",
            "format": "date_time"
            },
            {
            "field": "zeek.ocsp.update.this",
            "format": "date_time"
            },
            {
            "field": "zeek.pe.compile_time",
            "format": "date_time"
            },
            {
            "field": "zeek.smb_files.times.accessed",
            "format": "date_time"
            },
            {
            "field": "zeek.smb_files.times.changed",
            "format": "date_time"
            },
            {
            "field": "zeek.smb_files.times.created",
            "format": "date_time"
            },
            {
            "field": "zeek.smb_files.times.modified",
            "format": "date_time"
            },
            {
            "field": "zeek.smtp.date",
            "format": "date_time"
            },
            {
            "field": "zeek.snmp.up_since",
            "format": "date_time"
            },
            {
            "field": "zeek.x509.certificate.valid.from",
            "format": "date_time"
            },
            {
            "field": "zeek.x509.certificate.valid.until",
            "format": "date_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "_source": {
            "excludes": []
        },
        "query": {
            "bool": {
            "must": [],
            "filter": [
                {
                "bool": {
                    "should": [
                    {
                        "bool": {
                        "should": [
                            {
                            "match": {
                                "winlog.event_id": "102"
                            }
                            }
                        ],
                        "minimum_should_match": 1
                        }
                    },
                    {
                        "bool": {
                        "should": [
                            {
                            "match": {
                                "winlog.event_id": "201"
                            }
                            }
                        ],
                        "minimum_should_match": 1
                        }
                    },
                    {
                        "bool": {
                        "should": [
                            {
                            "match": {
                                "winlog.event_id": "4702"
                            }
                            }
                        ],
                        "minimum_should_match": 1
                        }
                    },
                    {
                        "bool": {
                        "should": [
                            {
                            "match": {
                                "winlog.event_id": "4698"
                            }
                            }
                        ],
                        "minimum_should_match": 1
                        }
                    },
                    {
                        "bool": {
                        "should": [
                            {
                            "match": {
                                "winlog.event_id": "4699"
                            }
                            }
                        ],
                        "minimum_should_match": 1
                        }
                    }
                    ],
                    "minimum_should_match": 1
                }
                },
                {
                "range": {
                    "@timestamp": {
                    "format": "strict_date_optional_time",
                    "gte": "2023-08-06T13:21:23.154Z",
                    "lte": "LTE_KEY_VALUE"
                    }
                }
                }
            ],
            "should": [],
            "must_not": []
            }
        }
        },
    "report_monitoring_new_services": {
        "size": 100,
        "sort": [
            {
            "@timestamp": {
                "order": "desc",
                "unmapped_type": "boolean"
            }
            }
        ],
        "fields": [
            {
            "field": "*",
            "include_unmapped": "true"
            },
            {
            "field": "@timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "dll.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.ingested",
            "format": "strict_date_optional_time"
            },
            {
            "field": "event.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "package.installed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.end",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.parent.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "process.start",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.first_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.last_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.modified_at",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.code_signature.timestamp",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.ctime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.elf.creation_date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.mtime",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.file.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.first_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.last_seen",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.modified_at",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "threat.indicator.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.client.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.x509.not_after",
            "format": "strict_date_optional_time"
            },
            {
            "field": "tls.server.x509.not_before",
            "format": "strict_date_optional_time"
            },
            {
            "field": "winlog.time_created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.kerberos.valid.from",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.kerberos.valid.until",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.org_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.rec_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.ref_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ntp.xmt_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.revoke.time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.update.next",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.ocsp.update.this",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.pe.compile_time",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.accessed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.changed",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.created",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smb_files.times.modified",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.smtp.date",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.snmp.up_since",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.x509.certificate.valid.from",
            "format": "strict_date_optional_time"
            },
            {
            "field": "zeek.x509.certificate.valid.until",
            "format": "strict_date_optional_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "query": {
            "bool": {
            "must": [],
            "filter": [
                {
                "bool": {
                    "should": [
                    {
                        "match": {
                        "winlog.event_id": "4697"
                        }
                    }
                    ],
                    "minimum_should_match": 1
                }
                },
                {
                "range": {
                    "@timestamp": {
                    "format": "strict_date_optional_time",
                    "gte": "2023-08-06T13:33:00.996Z",
                    "lte": "LTE_KEY_VALUE"
                    }
                }
                }
            ],
            "should": [],
            "must_not": []
            }
        }
        },
    "report_monitoring_rare_powershell": {
        "aggs": {
            "0": {
            "rare_terms": {
                "field": "winlog.event_data.Path",
                "max_doc_count": 4
            }
            }
        },
        "size": 0,
        "fields": [
            {
            "field": "@timestamp",
            "format": "date_time"
            },
            {
            "field": "dll.code_signature.timestamp",
            "format": "date_time"
            },
            {
            "field": "event.created",
            "format": "date_time"
            },
            {
            "field": "event.end",
            "format": "date_time"
            },
            {
            "field": "event.ingested",
            "format": "date_time"
            },
            {
            "field": "event.start",
            "format": "date_time"
            },
            {
            "field": "file.accessed",
            "format": "date_time"
            },
            {
            "field": "file.code_signature.timestamp",
            "format": "date_time"
            },
            {
            "field": "file.created",
            "format": "date_time"
            },
            {
            "field": "file.ctime",
            "format": "date_time"
            },
            {
            "field": "file.elf.creation_date",
            "format": "date_time"
            },
            {
            "field": "file.mtime",
            "format": "date_time"
            },
            {
            "field": "file.x509.not_after",
            "format": "date_time"
            },
            {
            "field": "file.x509.not_before",
            "format": "date_time"
            },
            {
            "field": "package.installed",
            "format": "date_time"
            },
            {
            "field": "process.code_signature.timestamp",
            "format": "date_time"
            },
            {
            "field": "process.elf.creation_date",
            "format": "date_time"
            },
            {
            "field": "process.end",
            "format": "date_time"
            },
            {
            "field": "process.parent.code_signature.timestamp",
            "format": "date_time"
            },
            {
            "field": "process.parent.elf.creation_date",
            "format": "date_time"
            },
            {
            "field": "process.parent.end",
            "format": "date_time"
            },
            {
            "field": "process.parent.start",
            "format": "date_time"
            },
            {
            "field": "process.start",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.accessed",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.code_signature.timestamp",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.created",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.ctime",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.elf.creation_date",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.mtime",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_after",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.file.x509.not_before",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.first_seen",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.last_seen",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.modified_at",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_after",
            "format": "date_time"
            },
            {
            "field": "threat.enrichments.indicator.x509.not_before",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.accessed",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.code_signature.timestamp",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.created",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.ctime",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.elf.creation_date",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.mtime",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.x509.not_after",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.file.x509.not_before",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.first_seen",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.last_seen",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.modified_at",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.x509.not_after",
            "format": "date_time"
            },
            {
            "field": "threat.indicator.x509.not_before",
            "format": "date_time"
            },
            {
            "field": "tls.client.not_after",
            "format": "date_time"
            },
            {
            "field": "tls.client.not_before",
            "format": "date_time"
            },
            {
            "field": "tls.client.x509.not_after",
            "format": "date_time"
            },
            {
            "field": "tls.client.x509.not_before",
            "format": "date_time"
            },
            {
            "field": "tls.server.not_after",
            "format": "date_time"
            },
            {
            "field": "tls.server.not_before",
            "format": "date_time"
            },
            {
            "field": "tls.server.x509.not_after",
            "format": "date_time"
            },
            {
            "field": "tls.server.x509.not_before",
            "format": "date_time"
            },
            {
            "field": "winlog.time_created",
            "format": "date_time"
            },
            {
            "field": "zeek.kerberos.valid.from",
            "format": "date_time"
            },
            {
            "field": "zeek.kerberos.valid.until",
            "format": "date_time"
            },
            {
            "field": "zeek.ntp.org_time",
            "format": "date_time"
            },
            {
            "field": "zeek.ntp.rec_time",
            "format": "date_time"
            },
            {
            "field": "zeek.ntp.ref_time",
            "format": "date_time"
            },
            {
            "field": "zeek.ntp.xmt_time",
            "format": "date_time"
            },
            {
            "field": "zeek.ocsp.revoke.time",
            "format": "date_time"
            },
            {
            "field": "zeek.ocsp.update.next",
            "format": "date_time"
            },
            {
            "field": "zeek.ocsp.update.this",
            "format": "date_time"
            },
            {
            "field": "zeek.pe.compile_time",
            "format": "date_time"
            },
            {
            "field": "zeek.smb_files.times.accessed",
            "format": "date_time"
            },
            {
            "field": "zeek.smb_files.times.changed",
            "format": "date_time"
            },
            {
            "field": "zeek.smb_files.times.created",
            "format": "date_time"
            },
            {
            "field": "zeek.smb_files.times.modified",
            "format": "date_time"
            },
            {
            "field": "zeek.smtp.date",
            "format": "date_time"
            },
            {
            "field": "zeek.snmp.up_since",
            "format": "date_time"
            },
            {
            "field": "zeek.x509.certificate.valid.from",
            "format": "date_time"
            },
            {
            "field": "zeek.x509.certificate.valid.until",
            "format": "date_time"
            }
        ],
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "_source": {
            "excludes": []
        },
        "query": {
            "bool": {
            "must": [],
            "filter": [
                {
                "range": {
                    "@timestamp": {
                    "format": "strict_date_optional_time",
                    "gte": "2023-08-06T13:50:14.530Z",
                    "lte": "LTE_KEY_VALUE"
                    }
                }
                }
            ],
            "should": [],
            "must_not": []
            }
        }
        }
}