#!/usr/bin/bash

LOG_FILES=(     "Windows PowerShell.evtx" 
                "Security.evtx" 
                "System.evtx" 
                "Microsoft-Windows-WinRM%4Operational.evtx" 
                "Microsoft-Windows-Windows Firewall With Advanced Security%4Firewall.evtx" 
                "Microsoft-Windows-Windows Defender%4Operational.evtx" 
                "Microsoft-Windows-TerminalServices-RemoteConnectionManager%4Operational.evtx" 
                "Microsoft-Windows-TerminalServices-RDPClient%4Operational.evtx" 
                "Microsoft-Windows-TaskScheduler%4Operational.evtx" 
                "Microsoft-Windows-TaskScheduler%4Operational.evtx" 
                "Microsoft-Windows-RemoteDesktopServices-RdpCoreTS%4Operational.evtx" 
                "Microsoft-Windows-Sysmon%4Operational.evtx" 
                "Microsoft-Windows-PowerShell%4Operational.evtx"
)
IFS=""

BASE_PATH="/home/so/screening/output"
BASE=`basename $1 .zip`
unzip $1 -d $BASE_PATH 
SOURCE="${BASE_PATH}/$BASE/logs/"
IMPORTED_SOURCE=$SOURCE/imported
mkdir $IMPORTED_SOURCE
for log in ${LOG_FILES[*]}
do
    echo "Processing ${log} in location ${SOURCE}"
    sudo so-import-evtx "${SOURCE}/${log}"
    cp "${SOURCE}/${log}" $IMPORTED_SOURCE
done

echo "---------------------------------------------"
echo "---------------------------------------------"
echo "Now run the process-asset.sh script to import data in Elastic; then process with Chainsaw"
echo ""
echo "screening/scripts/2-process-asset.sh ${BASE}"
echo "screening/scripts/3-process-chainsaw.sh ${IMPORTED_SOURCE}"
echo ""
