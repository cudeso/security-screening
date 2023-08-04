@echo off

:: 1/
:: The returned date format is different per Windows version and regional setting
:: Windows 10: %DATE:~6,4%%DATE:~3,2%%DATE:~0,2%
:: Windows 7:  %DATE:~10,4%%DATE:~4,2%%DATE:~7,2%
::
:: Procedure to get the correct format. 
:: Use 'echo %DATE%' in a console
:: Then count the position of the year (start with 0). 
:: In Windows 10, year starts at position 6, uses 4 characters
:: Then do the same for month. In Windows 10, starts at position 3, uses 2 characters
:: Finally for the day, starts at 0 (begin of string), uses 2 characters
::
:: 2/
:: Make sure "7za" is in the same folder as the batch file
::
:: 3/
:: Run as Administrator
::

set parsed_date=%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%
set aud_dir=audit_%COMPUTERNAME%_%parsed_date%
set script_dir=%~dp0

mkdir "%SystemRoot%\Temp\logs_copy"
xcopy /E/H/C/I "%SystemRoot%\System32\Winevt\Logs" "%SystemRoot%\Temp\logs_copy"
"%script_dir%7za.exe" a -bd -tzip %script_dir%%aud_dir%.zip "%SystemRoot%\Temp\logs_copy"
del /f /q "%SystemRoot%\Temp\logs_copy\*"
rmdir /q "%SystemRoot%\Temp\logs_copy\
