# General

The scripts are not signed. Temporarily set a more relaxed ExecutionPolicy.

# hunt-archive-files.ps1

## Setup

- Update the **username** to an existing username 
  - `$user = "joe"`
- Make sure there is a **directory** `hunt` on the Desktop of that user
  - `c:\Users\$user\Desktop\hunt`

## Define targets

- Set the **directories** that need to be monitored in `$directories`
  - Include the directories where users commonly store scripts
    - `d:\`?
  - Users directory
    - `c:\Users\`
  - Windows temp
    - `c:\Windows\temp\`
  - Temp
    - `c:\temp\`
- Example: 
  - `$directories = @("c:\Users\", "c:\Windows\Temp\", "c:\temp\")`

## Run

- Run the script as **Administrator**. You're collecting scripts from other users, and likely need elevated permissions.

## Output

- A CSV file `c:\Users\$user\Desktop\hunt\hunt-archive-files.csv` with these fields
  - `FullPath,Name,Extension,Size (bytes),CreationDate,LastModifiedDate`
- A ZIP file with the scripts content `c:\Users\$user\Desktop\hunt\hunt-archive-files.zip`

# hunt-get-file-details.ps1

## Setup

- Update the **username** to an existing username 
  - `$user = "joe"`
- Make sure there is a **directory** `hunt` on the Desktop of that user
  - `c:\Users\$user\Desktop\hunt`

## Define targets

- Set the **directories** that need to be monitored in `$directories`
  - Include Inetweb (can be c: or d:)
    - `c:\inetpub\wwwroot` and `d:\inetpub\wwwroot`
  - Windows temp
    - `c:\Windows\temp\`
  - Temp
    - `c:\temp\`
  - Users Public
    - `C:\Users\Public`
  - SysWOW64
    - `C:\Windows\SysWOW64`
  - AppData
    - `C:\Windows\System32\config\systemprofile\AppData\Local\Microsoft\Windows`
- Example:
    - `$directories = @("C:\inetpub\wwwroot", "C:\Windows\Temp", "C:\Temp", "C:\Windows\SysWOW64", "C:\Users\Public", "C:\Windows\System32\config\systemprofile\AppData\Local\Microsoft\Windows")`
- Set the f**ile extensions** that need to be monitored in `$fileextensions`
  - `$fileextensions = @(".exe", ".ps1", ".dll", ".com", "vbs", ".js", ".pl", ".sh", ".py", ".cpl", ".cab", ".bat", ".cmd", ".lnk", ".msi", ".pif", ".scr", ".vbe", ".ws", ".wsh", ".rar", ".zip", ".7z", ".gz", ".sqlite", ".db")`

## Run

- Run the script as **Administrator**. You're binaries in various locations, and likely need elevated permissions.

## Output

- A CSV file `c:\Users\$user\Desktop\hunt\hunt-filedetails.csv` with these fields
  - `FullPath,Name,Extension,Size (bytes),CreationDate,LastModifiedDate,MD5,SHA256,OriginalFilename,ProductVersion,FileVersion,CompileTimestamp,FileDescription,CompanyName,FileLanguage,SignatureSubject,SignatureTimestamp,SignatureSigningAlgo,SignatureIssuer,SignatureSerial`

# hunt-get-lnk-files.ps1

## Setup

- Update the **username** to an existing username 
  - `$user = "joe"`
- Make sure there is a **directory** `hunt` on the Desktop of that user
  - `c:\Users\$user\Desktop\hunt`

## Define targets

- Set the **directories** that need to be monitored in `$directories`
  - Users directory
    - `c:\Users\`
  - Windows temp
    - `c:\Windows\temp\`
  - Temp
    - `c:\temp\`
- Example:
  - `$directories = @("c:\Users\", "c:\Windows\Temp\", "c:\temp\")`
- Leave the file extensions unchanged, configred as `@$fileextensions = @(".lnk")`

## Run

- Run the script as **Administrator**. You're binaries in various locations, and likely need elevated permissions.

## Output

- A CSV file `c:\Users\$user\Desktop\hunt\hunt-lnk-files.csv` with these fields
  - `FullPath,Name,Extension,Size (bytes),CreationDate,LastModifiedDate,LNKTarget`

# hunt-get-additional-details.ps1

## Setup

- Update the **username** to an existing username 
  - `$user = "joe"`
- Make sure there is a **directory** `hunt` on the Desktop of that user
  - `c:\Users\$user\Desktop\hunt`
- Make sure the SysInternals tool **AutoRuns** is available in the folder `..\supporttools\autorunsc64.exe`
  - That's one level up; alternatively specify a different location
  - Copy the folder `supporttools`

## Define targets

- Targets are predefined the script. No changes are required;
- 
## Run

- Run the script as **Administrator**. You're binaries in various locations, and likely need elevated permissions.

## Output

- Multiple CSV files 
  - `c:\Users\$user\Desktop\hunt\hunt-autorunsc64.csv` with these fields
    - `Time,Entry Location,Entry,Enabled,Category,Profile,Description,Signer,Company,Image Path,Version,Launch String,MD5,SHA-1,PESHA-1,PESHA-256,SHA-256,IMP`
  - `c:\Users\$user\Desktop\hunt\hunt-EventFilters.csv` with these fields
    - `"Name","Query","EventNamespace"`
  - `c:\Users\$user\Desktop\hunt\hunt-NetworkConnections.csv` with these fields
    - `"LocalAddress","LocalPort","RemoteAddress","RemotePort","State","OwningProcess"`
  - `c:\Users\$user\Desktop\hunt\hunt-NetworkConnectionsOld.csv` text dump, no CSV
  - `c:\Users\$user\Desktop\hunt\hunt-Process.csv` with these fields
    - `"ProcessId","Caption","ExecutablePath","CreationDate","ParentProcessId","SessionId","CommandLine"`
  - `c:\Users\$user\Desktop\hunt\hunt-SchTasks.csv` with these fields
    - `"HostName","TaskName","Next Run Time","Status","Logon Mode","Last Run Time","Last Result","Author","Task To Run","Start In","Comment","Scheduled Task State","Idle Time","Power Management","Run As User","Delete Task If Not Rescheduled","Stop Task If Runs X Hours and X Mins","Schedule","Schedule Type","Start Time","Start Date","End Date","Days","Months","Repeat: Every","Repeat: Until: Time","Repeat: Until: Duration","Repeat: Stop If Still Running"`
  - `c:\Users\$user\Desktop\hunt\hunt-Services.csv` with these fields
    - `"Name","DisplayName","PathName","StartMode","State","StartName","InstallDate"`
  - `c:\Users\$user\Desktop\hunt\hunt-registry.csv` with these fields
    - `"PSChildName","HKLM:\Software\Microsoft\Windows\CurrentVersion\Run","Length"`
  - `c:\Users\$user\Desktop\hunt\hunt-WMIProcesses.csv` with these fields
    - `"ProcessId","Name","CommandLine"`
