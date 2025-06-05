<#
.SYNOPSIS
    Get all autoruns, scheduled tasks, WMIC, processes, services, network connections and interesting registry keys

.DESCRIPTION

#>

$user = "public"

# Ensure the hunt directory exists
$huntDir = "C:\Users\$user\Desktop\hunt"
if (-not (Test-Path -Path $huntDir)) {
    New-Item -ItemType Directory -Path $huntDir | Out-Null
}

$schtaksOutput = "C:\Users\$user\Desktop\hunt\hunt-SchTasks.csv"
$processOutput = "C:\Users\$user\Desktop\hunt\hunt-Process.csv"
$eventFilterOutput = "C:\Users\$user\Desktop\hunt\hunt-EventFilters.csv"
$wmiProcessOutput = "C:\Users\$user\Desktop\hunt\hunt-WMIProcesses.csv"
$servicesOutput = "C:\Users\$user\Desktop\hunt\hunt-Services.csv"
$networkConnectionsOutput = "C:\Users\$user\Desktop\hunt\hunt-NetworkConnections.csv"
$networkConnectionsOutputOld = "C:\Users\$user\Desktop\hunt\hunt-NetworkConnectionsOld.csv"
$autorunsOutput = "C:\Users\$user\Desktop\hunt\hunt-autorunsc64.csv"
$registryOutput = "C:\Users\$user\Desktop\hunt\hunt-registry.csv"

Write-Host "Autoruns"
..\supporttools\autorunsc64.exe /accepteula -a * -c -h -s '*' -nobanner >$autorunsOutput

Write-Host "Scheduled tasks"
schtasks.exe /Query /V /FO CSV > $schtaksOutput

Write-Host "WMIC subscriptions"
Get-WmiObject -Namespace "root\subscription" -Class __EventFilter |  Select-Object Name, Query, EventNamespace | Export-Csv -Path $eventFilterOutput -NoTypeInformation
Get-WmiObject -Query "SELECT * FROM Win32_Process WHERE Name='wmiprvse.exe'" | Select-Object ProcessId, Name, CommandLine | Export-Csv -Path $wmiProcessOutput -NoTypeInformation

Write-Host "Processes"
Get-WmiObject -Query "SELECT * FROM Win32_Process" | Select-Object ProcessId, Caption, ExecutablePath, CreationDate, ParentProcessId, SessionId, CommandLine | Export-Csv -Path $processOutput -NoTypeInformation

Write-Host "Services"
Get-WmiObject -Class Win32_Service | Select-Object Name, DisplayName, PathName, StartMode, State, StartName, InstallDate | Export-Csv -Path $servicesOutput -NoTypeInformation

Write-Host "Network connections"
$networkConnections = Get-NetTCPConnection | Where-Object { $_.State -eq "Established" }
$networkConnections | Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State, OwningProcess | Export-Csv -Path $networkConnectionsOutput -NoTypeInformation
netstat -naob > $networkConnectionsOutputOld

Write-Host "Registry keys"
$autorunKeys = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce"
)
$autorunEntries = foreach ($key in $autorunKeys) {
    Get-ItemProperty -Path $key | Select-Object PSChildName, $key -ExpandProperty PSChildName
}
$autorunEntries | Export-Csv -Path $registryOutput -NoTypeInformation

Write-Host "Finished"
Write-Host "Outputs saved to:"
Write-Host "  $schtaksOutput"
Write-Host "  $processOutput"
Write-Host "  $eventFilterOutput"
Write-Host "  $wmiProcessOutput"
Write-Host "  $servicesOutput"
Write-Host "  $networkConnectionsOutput"
Write-Host "  $networkConnectionsOutputOld"
Write-Host "  $autorunsOutput"
Write-Host "  $registryOutput"