@ECHO OFF

:: Audit script v4
::  v1 : Start
::  v2 : Fixed fetching all users ; include localgroups
::           Removed bugs with jumping to wrong subs from v1
::  v3 : Included scheduled task and startup items
::  v4 : Fix spaces (line wrapping) for systeminfo_inventory.csv
::       Add whoami and gpresult data
::  v5 : Add copy etc/drivers/* files
::

set debug=0

:: Step 1
:: Get the computer name
:: Needed to create the output directory
if %debug%==1 echo "Fetching system name"
FOR /f "tokens=2,* delims= " %%a in ('IPCONFIG ^/ALL ^| FINDSTR "Primary Dns"') do set tempsuffix=%%b
FOR /f "tokens=1,2 delims=:" %%a in ('echo %tempsuffix%') do set dnssuffix=%%b
SET FQDN=%COMPUTERNAME%.%DNSSUFFIX:~1%

ECHO Server FQDN: %FQDN%
set aud_dir=audit_%FQDN%
mkdir %aud_dir%
cd %aud_dir%


:: Step 2
:: Operating system version and system information
if %debug%==1 echo "ver"
ver > ver.txt

if %debug%==1 echo "systeminfo"
systeminfo > systeminfo.txt
systeminfo /fo CSV > systeminfo.csv


:: Step 3
:: Grap info from systeminfo for inventory template
set inventory_hostname=
set inventory_osname=
set inventory_osversion=
set inventory_installdate=
set inventory_boottime=
set inventory_system_manufacturer=
set inventory_timezone=
set inventory_productid=

for /f "usebackq tokens=2 delims=:" %%s in (`type systeminfo.txt ^| findstr /B /C:"Host Name:"`) do (
 set inventory_hostname=%%s
)
for /f "usebackq tokens=2 delims=:" %%s in (`type systeminfo.txt ^| findstr /B /C:"OS Name:"`) do (
 set inventory_osname=%%s
)
for /f "usebackq tokens=2 delims=:" %%s in (`type systeminfo.txt ^| findstr /B /C:"OS Version:"`) do (
 set inventory_osversion=%%s
)
for /f "usebackq tokens=2,3,4 delims=:" %%s in (`type systeminfo.txt ^| findstr /C:"Original Install Date:"`) do (
 set inventory_installdate=%%s:%%t:%%u
)
for /f "usebackq tokens=2,3,4 delims=:" %%s in (`type systeminfo.txt ^| findstr /C:"System Boot Time:"`) do (
 set inventory_boottime=%%s:%%t:%%u
)
for /f "usebackq tokens=2 delims=:" %%s in (`type systeminfo.txt ^| findstr /B /C:"System Manufacturer:"`) do (
 set inventory_system_manufacturer=%%s
)
for /f "usebackq tokens=2,* delims=:" %%s in (`type systeminfo.txt ^| findstr /B /C:"Time Zone:"`) do (
 set inventory_timezone=%%s:%%t
)
for /f "usebackq tokens=2 delims=:" %%s in (`type systeminfo.txt ^| findstr /B /C:"Product ID:"`) do (
 set inventory_productid=%%s
)

for /f "tokens=* delims= " %%G in ("%inventory_hostname%") do set inventory_hostname=%%G
for /f "tokens=* delims= " %%G in ("%inventory_osname%") do set inventory_osname=%%G
for /f "tokens=* delims= " %%G in ("%inventory_osversion%") do set inventory_osversion=%%G
for /f "tokens=* delims= " %%G in ("%inventory_installdate%") do set inventory_installdate=%%G
for /f "tokens=* delims= " %%G in ("%inventory_boottime%") do set inventory_boottime=%%G
for /f "tokens=* delims= " %%G in ("%inventory_system_manufacturer%") do set inventory_system_manufacturer=%%G
for /f "tokens=* delims= " %%G in ("%inventory_timezone%") do set inventory_timezone=%%G
for /f "tokens=* delims= " %%G in ("%inventory_productid%") do set inventory_productid=%%G

echo %inventory_hostname% ; %FQDN% ; %inventory_osname% ; %inventory_osversion% ; %inventory_installdate% ; %inventory_boottime% ; %inventory_system_manufacturer% ; %inventory_timezone% ; %inventory_productid%  > systeminfo_inventory.csv


:: Step 4
:: User and account information
:: Service information
if %debug%==1 echo "net start"
net start > net_start.txt


if %debug%==1 echo "net user"
net user > net_user.txt
if %debug%==1 echo "net account"
net accounts > net_accounts.txt
if %debug%==1 echo "net use"
net use > net_use.txt
if %debug%==1 echo "net view"
net view > net_view.txt
if %debug%==1 echo "net use"
net config server >> net_config.txt
if %debug%==1 echo "net use"
net config workstation >> net_config.txt
if %debug%==1 echo "net localgroup"
net localgroup >> net_localgroup.txt
echo > net_localgroup_detail.txt

for /F "tokens=* eol=- skip=2" %%a in (net_localgroup.txt) do call :processlocalgroup %%a


if %debug%==1 echo "users"
echo > users_detail.txt

for /F "tokens=* delims=  eol=- skip=2" %%a in (net_user.txt) do call :processuser %%a




:: Step 5
:: Network information

if %debug%==1 echo "ipconfig dns"
ipconfig /displaydns > ipconfig_dnscache.txt

if %debug%==1 echo "ipconfig"
ipconfig /all > ipconfig_all.txt
if %debug%==1 echo "route"
route print > route_print.txt
if %debug%==1 echo "fw"
netsh firewall show state >> fw_config.txt
netsh firewall show config >> fw_config.txt
if %debug%==1 echo "rpc"
netsh rpc show >> rpc_config.txt

if %debug%==1 echo "netstat"
netstat -nao > netstat.txt

if %debug%==1 echo "netstat stats"
netstat -s > netstat_stats.txt

if %debug%==1 echo "arp"
arp -a > arp.txt
arp -a -v > arp_verbose.txt

if %debug%==1 echo "nbtstat"
nbtstat -n > nbtstat_n.txt
nbtstat -c > nbtstat_c.txt
nbtstat -s > nbtstat_s.txt


:: Step 6
:: Running procecess
if %debug%==1 echo "ps"
tasklist > tasklist.txt
tasklist /v > tasklist_verbose.txt
tasklist /SVC > tasklist_svc.txt
tasklist /v /FO CSV > tasklist.csv
tasklist /SVC /FO CSV > tasklist_svc.csv

:: Step 7
:: Installed software
:: Installed services

if %debug%==1 echo "installed"

echo ================= >>software_list.txt
reg export HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall temp1.txt
find "DisplayName" temp1.txt| find /V "ParentDisplayName" > temp2.txt
for /f "tokens=2,3 delims==" %%a in (temp2.txt) do (echo %%a >> software_list.txt)
del temp1.txt
del temp2.txt

for /f "usebackq tokens=1,2,3 delims=:" %%i in (`sc query state^= all`) do (
  rem echo %%i %%j %%k
  if "%%i"=="SERVICE_NAME" call :%%i %%j %%k
)


:: Step 8
:: Policies
gpresult /r > gpresult.txt


:: Step 9
:: Log configuration setup
wevtutil gl Application > log_config_application.txt
wevtutil gli Application >> log_config_application.txt
wevtutil gl Security > log_config_security.txt
wevtutil gli Security >> log_config_security.txt
wevtutil gl Setup > log_config_setup.txt
wevtutil gli Setup >> log_config_setup.txt
wevtutil gl System > log_config_system.txt
wevtutil gli System >> log_config_system.txt


wevtutil qe Security > log_security.txt
wevtutil qe System > log_system.txt


:: Step 10
:: USB Information
reg export "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USB" reg_enum_usb.txt
copy %SYSTEMROOT%\inf\setupapi.app.log .
copy %SYSTEMROOT%\inf\setupapi.dev.log .


:: Step 11
:: Driver Information
driverquery > driverquery.txt
driverquery /v /FO CSV > driverquery.csv


:: Step 12
:: Get scheduled tasks 
schtasks /query /FO CSV /V >schtasks.csv


:: Step 13
:: Get startup items 
wmic /output:wmic_startup.csv startup list full /format:"%WINDIR%\System32\wbem\en-us\csv"


:: Step 14
:: Get whoami information
whoami /user /fo csv > whoami_user.csv
whoami /groups /fo csv > whoami_groups.csv
whoami /priv /fo csv > whoami_priv.csv


:: Step 15
:: Get group policy results
gpresult /r > gpresult_summary.txt


:: Step 16
:: Copy files from drivers/drivers_etc_networks
copy %windir%\system32\drivers\etc\networks drivers_etc_networks
copy %windir%\system32\drivers\etc\hosts drivers_etc_hosts


:: END

exit /b


:: SUBROUTINES

:processlocalgroup 
set mygroup=%*
set mygroup2=%mygroup:~1,200%

echo %mygroup2% >> net_localgroup_detail.txt
echo ------------- >>  net_localgroup_detail.txt
net localgroup %mygroup2% >> net_localgroup_detail.txt
echo >> net_localgroup_detail.txt


:processuser
if {%1}=={} goto :end_user
net user %1 >> users_detail.txt

shift
goto :processuser 

:end_user


:SERVICE_NAME
::  echo %0 %1 %2
  set a=%1
  set a=%a:(=_%
  set a=%a:)=_%
  if     "%2"==""   call :process-service %a%
  if not "%2"=="" call :process-service %a%$%2


:process-service
::if %debug%==1 echo service "%1"

  set service_display_name=
  set service_name=
  set service_pid=
  set service_properties=
  set service_state=
  set service_type=
:: `sc query` and `sc queryex` will only show DISPLAY_NAME when no SERVICE_NAME is specified
:: so we have to perform `sc query` for ALL services, then grab the DISPLAY_NAME for the matching SERVICE_NAME
  for /f "usebackq tokens=1,* delims=:, " %%s in (`sc query state^= all`) do (
    rem if "%%s"=="STATE" if not !%1!==!! echo %%v state of %1 is %%v
    if "%%s"=="SERVICE_NAME" set service_name=%%t
    if "%%s"=="DISPLAY_NAME" if "!service_name!"=="%1" set service_display_name=%%t
    set first_char=%%s
    set first_char=!first_char:~0,1!
    if "!first_char!"=="(" if "!service_name!"=="%1" set service_properties=%%s, %%t
    rem echo "!first_char!", !service_properties!, %%s, %%t
  )
  set service_name=
:: find all services by SERVICE_NAME, then list STATE, TYPE, DISPLAY_NAME, and "" (this is on the line below STATE)
  for /f "usebackq tokens=1,2,3,4 delims=:, " %%s in (`sc queryex %1`) do (
    rem if "%%s"=="STATE" if not !%1!==!! echo %%v state of %1 is %%v
    if "%%s"=="PID" set service_pid=%%t
    if "%%s"=="SERVICE_NAME" set service_name=%%t
    if "%%s"=="STATE" set service_state=%%u
    if "%%s"=="STATE" set service_state=%%u
    if "%%s"=="TYPE" set service_type=%%u
    if "%%s"=="STATE" set service_state=%%u
    rem echo "%%s", "%%t", "%%u", "%%v"
  )
  echo %service_pid%, %service_state%, %service_type%, %service_name%, %service_properties%, %service_display_name% >> SERVICE_list.txt

