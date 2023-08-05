config = {
    "appname": "security screening",
    "logfile": "security-screening.log",
    "logfile_maxsize": 5000000,  # bytes
    "output_path": "/home/analyst/security-screening/securityonion/output",
    "input_path": "/home/analyst/security-screening/securityonion/input",
    "evtx_logs_to_process": ["Windows PowerShell.evtx",
                                "Security.evtx",
                                "System.evtx",
                                "Microsoft-Windows-WinRM%4Operational.evtx",
                                "Microsoft-Windows-Windows Firewall With Advanced Security%4Firewall.evtx",
                                "Microsoft-Windows-Windows Defender%4Operational.evtx",
                                "Microsoft-Windows-TerminalServices-RemoteConnectionManager%4Operational.evtx",
                                "Microsoft-Windows-TerminalServices-RDPClient%4Operational.evtx",
                                "Microsoft-Windows-TaskScheduler%4Operational.evtx",
                                "Microsoft-Windows-RemoteDesktopServices-RdpCoreTS%4Operational.evtx",
                                "Microsoft-Windows-Sysmon%4Operational.evtx",
                                "Microsoft-Windows-PowerShell%4Operational.evtx"
                                ],
    "evtx_hashed_to_skip": [ "a55fe49683c29388694af6ac8d49b480" ],                                
    "so-import-evtx": "/usr/sbin/so-import-evtx",
    "nsm_evtx": "/nsm/import/",
    "screening_session": "2023",
    "elasticsearch_index": "screening-results-ics",
    "elasticsearch_host": "https://127.0.0.1:9200",
    "elasticsearch_api_key": "",
    "elasticsearch_verify_certs": False,
    "elasticsearch_max_results": "999",
    "ignore_software": [
            'ATI Display Driver',
            'Altiris Deployment Agent',
            'Common Files',
            'Database Engine Services',
            'Database Engine Shared',
            'DirectX for Managed Code Update',
            'Hotfix for Microsoft',
            'Hotfix for Office',
            'Hotfix for Windows',
            'Intel Trusted Connect Service Client',
            'Intel(R) Chipset Device Software',
            'Intel(R) Graphics Media Accelerator Driver',
            'Intel(R) Management Engine Components',
            'Intel(R) Network Connections',
            'Intel(R) PRO Network Connections',
            'Intel(R) PRO/Wireless Driver',
            'PROSet/Wireless Software',
            'PROSet/Wireless WiFi Software',
            'Trusted Connect Service Client',
            'Intel(R) Processor Graphics',
            'Intel(R) Rapid Storage Technology',
            'Intel(R) Ready Mode Technology',
            'Intel(R) SDK for OpenCL - CPU Only Runtime Package',
            'Intel(R) USB 3.0 eXtensible Host Controller Driver',
            'Intel(R) Update Manager',
            'McAfee Agent',
            'McAfee Data Exchange Layer for MA',
            'McAfee DLP Endpoint',
            'McAfee Endpoint Security Platform',
            'McAfee Endpoint Security Threat PreventionMcAfee DLP Endpoint',
            'McAfee VirusScan Enterprise',
            'Microsoft .NET Framework',
            'Microsoft Application Error Reporting',
            'Microsoft Group Policy Management',
            'Microsoft Internationalized',
            'Microsoft Kernel-Mode',
            'Microsoft National Language',
            'Microsoft Office Proof',
            'Microsoft Policy Platform',
            'Microsoft Visual',
            'Microsoft WSE',
            'Microsoft XML Parser',
            'NVMe Drive Eject NMI Fix',
            'ODBC Driver',
            'R2 RsFx Driver',
            'R2 SP1 Database Engine Shared',
            'Security Update for',
            'Server Customer Experience Improvement',
            'Update for Microsoft Office',
            'Update for MicrosoftMicrosoft Office Shared',
            'Update for Windows Internet Explorer',
            'Update for Windows Server',
            'Update for Windows XP',
            'VMware Tools',
            'Veeam Agent for Microsoft Windows',
            'Veritas System Recovery 18',
            'Virtual Serial Port Driver',
            'Visual C++ 2008 x86 Runtime',
            'WinSCP',
            'Windows Genuine Advantage',
            'Windows Imaging Component',
            'Windows Internet Explorer',
            'Windows Support Tools',
            'Windows XP Hotfix',
            'XML Paper Specification Shared Components',
            ],
    "antimalware_software": ['MsMpEng.exe', 'mcshield.exe', 'Mcshield.exe'],
    "drop_es_index": False,
    "execute_chainsaw": False,
    "chainsaw_app": "../chainsaw/chainsaw_x86_64-unknown-linux-mus",
    "chainsaw_sigma": "../chainsaw/sigma/",
    "chainsaw_rules": "../chainsaw/rules/",
    "chainsaw_mappings": "screening_chainsaw-mappings-cudeso.yml",
    "always_import": True,
    "keep_output_files": False,
    "import_state_file": "/nsm/security-screening/securityonion/scripts/import_state.float",
	"always_delete_outputfiles": True,
    "processevtx_logfolder": False, #"logs_copy",
    "deletematchinglogs": False,
}
