# Usage

## Before
1. Copy the folder `security-screening` to a USB drive

## Audit
1. Insert the USB in the machine you whish to audit
3. Start a CMD prompt with `administrator` privileges. Do this via right-click, Choose "Run as administrator". Do not just run it as a user with administrator privileges, the "Run as administrator" is important.
4. Go to the path of `security-screening` on the USB drive (most often `cd d:\security-screening`)
5. Start the auditscript with `./auditscript.bat`
6. Let the script run until it's completely finished. This can take a long (>15 minutes) time.
7. Verify that there is a file `audit_<SYSTEMNAME>.zip`
8. Close the CMD prompt
9.  Right click on the USB and eject the USB drive

The zip file "audit_<SYSTEMNAME>.zip" contains all the evidences.
