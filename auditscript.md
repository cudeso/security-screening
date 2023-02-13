# Workflow

* Execution of Windows-native commands
* * Output is in txt or csv
* Copy all (non-open) event log files
* * Files stored in a directory audit_ with system name
* Also executes some tools from Sysinternals
* * Make sure that they are in the folder **supporttools**
* * * autorunsc64.exe
* * * csvde.exe
* * * psinfo64.exe
* * * psloggedon64.exe
* Then ZIPs all files in the directory audit_
* Deletes the audit_ folder

# Usage

1. Copy folder security-screening to USB
2. Insert USB in machine to audit
3. Open Explorer, go to USB drive
4. Right click on "auditscript.bat"
5. Choose "Run as administrator"
6. Let the script run until it's completely finished (the new "bat" window will close). This can take a long (>15 minutes) time
7. Verify that there is a file "audit_<SYSTEMNAME>.zip"
8. Right click on the USB and eject the USB drive

The zip file "audit_<SYSTEMNAME>.zip" contains all the evidences.
