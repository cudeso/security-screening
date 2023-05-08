import logging
from config import config
from termcolor import colored



def lookup_application(port, image_name, session_name):
    i_port = int(port)

    if port == "135" and image_name == "svchost.exe" and session_name == "Services":
        return "Windows File&Print sharing"
    elif port == "445" and image_name == "System" and session_name == "Services":
        return "Windows File&Print sharing"
    elif port == "135" and image_name == "svchost.exe" and session_name == "Console":
        return "Windows File&Print sharing"
    elif port == "445" and image_name == "System" and session_name == "Console":
        return "Windows File&Print sharing"
    elif port == "554" and image_name == "wmpnetwk.exe" and session_name == "Services":
        return "Windows Media Player Network Sharing Service"
    elif port == "623" and image_name == "LMS.exe" and session_name == "Services":
        return "Intel Manageability Service"
    elif port == "16992" and image_name == "LMS.exe" and session_name == "Services":
        return "Intel Manageability Service"
    elif port == "902" and image_name == "vmware-authd.exe" and session_name == "Services":
        return "VMware"
    elif port == "912" and image_name == "vmware-authd.exe" and session_name == "Services":
        return "VMware"
    elif image_name == "aaBootstrap.exe" or image_name == "aaLogger.exe" or image_name == "aaEngine.exe" or image_name == "aaLicServer.exe":
        return "Schneider Electric"
    elif port == "2869" and image_name == "System" and session_name == "Services":
        return "SSDP"
    elif port == "3389" and image_name == "svchost.exe" and session_name == "Services":
        return "RDP"
    elif port == "5413" and image_name == "slssvc.exe" and session_name == "Services":
        return "Wonderware"
    elif port == "2000" and image_name == "wwlogsvc.exe" and session_name == "Console":
        return "Wonderware"
    elif port == "2002" and image_name == "wwlogsvc.exe" and session_name == "Console":
        return "Wonderware"
    elif port == "5800" and image_name == "tvnserver.exe" and session_name == "Services":
        return "VNC"
    elif port == "5900" and image_name == "tvnserver.exe" and session_name == "Services":
        return "VNC"
    elif port == "5800" and image_name == "vncserver.exe":
        return "VNC"
    elif port == "5900" and image_name == "vncserver.exe":
        return "VNC"
    elif port == "5800" and image_name == "winvnc.exe":
        return "VNC"
    elif port == "5900" and image_name == "winvnc.exe":
        return "VNC"
    elif port == "102" and image_name == "s7oiehsx64.exe" and session_name == "Services":
        return "Siemens"
    elif port == "4410" and image_name == "almsrv64x.exe" and session_name == "Services":
        return "Siemens"
    elif port == "10243" and image_name == "System" and session_name == "Services":
        return "SSDP"
    elif port == "2103" and image_name == "mqsvc.exe" and session_name == "Services":
        return "Microsoft Message Queuing"
    elif port == "2104" and image_name == "mqsvc.exe" and session_name == "Services":
        return "Microsoft Message Queuing"
    elif port == "2105" and image_name == "mqsvc.exe" and session_name == "Services":
        return "Microsoft Message Queuing"
    elif port == "2106" and image_name == "mqsvc.exe" and session_name == "Services":
        return "Microsoft Message Queuing"
    elif port == "2107" and image_name == "mqsvc.exe" and session_name == "Services":
        return "Microsoft Message Queuing"
    elif port == "49171" and image_name == "mqsvc.exe" and session_name == "Services":
        return "Microsoft Message Queuing"
    elif port == "49172" and image_name == "mqsvc.exe" and session_name == "Services":
        return "Microsoft Message Queuing"
    elif port == "5040" and image_name == "svchost.exe" and session_name == "Services":
        return "Windows Deployment Services server"
    elif port == "6183" and image_name == "Veeam.EndPoint.Service.exe":
        return "Veeam"
    elif port == "6184" and image_name == "Veeam.EndPoint.Service.exe":
        return "Veeam"
    elif port == "9395" and image_name == "Veeam.EndPoint.Service.exe":
        return "Veeam"
    elif port == "7937" and image_name == "nsrexecd.exe":
        return "EMC Networker"
    elif port == "7938" and image_name == "nsrexecd.exe":
        return "EMC Networker"
    elif port == "8229" and image_name == "nsrexecd.exe":
        return "EMC Networker"
    elif port == "8311" and image_name == "nsrexecd.exe":
        return "EMC Networker"
    elif port == "8381" and image_name == "nsrexecd.exe":
        return "EMC Networker"
    elif port == "8318" and image_name == "nsrexecd.exe":
        return "EMC Networker"
    elif port == "8000" and image_name == "nsrexecd.exe":
        return "EMC Networker"
    elif port == "8325" and image_name == "nsrexecd.exe":
        return "EMC Networker"
    elif port == "8081" and image_name == "macmnsvc.exe":
        return "McAfee"
    elif port == "49173" and image_name == "mqsvc.exe" and session_name == "Services":
        return "Veritas Enterprise Vault"
    elif port == "2031" and image_name == "ThinClientService.exe" and session_name == "Console":
        return "Rockwell - Thinmanager"
    elif port == "2031" and image_name == "ThinServer.exe" and session_name == "Console":
        return "Rockwell - Thinmanager"
    elif port == "5900" and image_name == "WinTMCShadow.exe" and session_name == "Console":
        return "Rockwell - Thinmanager"
    elif port == "65535" and image_name == "WinTMCShadow.exe" and session_name == "Console":
        return "Rockwell - Thinmanager"
    elif i_port > 49151 and (image_name == "services.exe" or image_name == "svchost.exe" or image_name == "wininit.exe" or image_name == "lsass.exe") and session_name == "Services":
        return "RPC-Client"
    elif i_port > 49151 and image_name == "aaLogger.exe" and session_name == "Services":
        return "Wonderware"
    elif i_port == 1027 and image_name == "aaLogger.exe" and session_name == "Services":
        return "Wonderware"
    elif i_port > 49151 and image_name == "aaBootstrap.exe" and session_name == "Services":
        return "Wonderware"
    elif i_port > 49100 and image_name == "CCEServer.exe" and session_name == "Services":
        return "Siemens"
    elif i_port > 49100 and image_name == "sqlservr.exe" and session_name == "Services":
        return "SQL Server"
    elif port == "1433" and image_name == "sqlservr.exe":
        return "SQL Server"
    elif port == "3306" and image_name == "mysqld.exe":
        return "MySQL"
    elif port == "3307" and image_name == "mysqld.exe":
        return "MySQL"
    elif i_port == 16388 and image_name == "ssc_service_x.exe":
        return "SIMATIC"
    elif i_port == 4410 and image_name == "almsrvx.exe":
        return "Siemens"
    elif i_port > 49100 and image_name == "UNS.exe" and session_name == "Services":
        return "Intel Manageability Service"
    elif i_port == 80 and image_name == "System" and session_name == "Services":
        return "Web service"
    elif i_port == 443 and image_name == "System" and session_name == "Services":
        return "Web service"        
    return ""
