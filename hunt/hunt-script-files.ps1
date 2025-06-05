<#
.SYNOPSIS
    Collect all script files


.DESCRIPTION
    Collect installed scripts on a system (full content of the scripts). Store script files in a ZIP. CSV file with path, script filename, date, size
#>


# Function to process files in a directory recursively
function Process-FilesRecursively {
    param (
        [string]$directory,
        [string[]]$fileextensions,
        [string]$zipFile
    )

    # Get all files and directories in the directory
    $items = Get-ChildItem -Path $directory

    # Loop through each item
    foreach ($item in $items) {        
        if ($item -is [System.IO.FileInfo]) {
            if ($item.Extension -in $fileextensions) {
                Process-File $item $zipFile
            }
        }
        elseif ($item -is [System.IO.DirectoryInfo]) {
            # If it's a directory, recursively process its files
            Process-FilesRecursively -directory $item.FullName -fileextensions $fileextensions -zipFile $zipFile
        }
    }
}

# Function to process a single file
function Process-File {
    param (
        [System.IO.FileInfo]$file,
        [string]$zipFile
    )

    $fullPath = $file.FullName
    $name = $file.Name
    $size = $file.Length
    $extension = $file.Extension
    $creationDate = $file.CreationTime
    $lastModifiedDate = $file.LastWriteTime

    # Add the file to the ZIP archive
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $zipArchive = [System.IO.Compression.ZipFile]::Open($zipFile, 'Update')
    $entry = $zipArchive.CreateEntry($name)
    $fileStream = $entry.Open()
    $stream = [System.IO.File]::OpenRead($fullPath)
    $stream.CopyTo($fileStream)
    $fileStream.Close()
    $stream.Close()
    $zipArchive.Dispose()

    "$fullPath,$name,$extension,$size,$creationDate,$lastModifiedDate" | Out-File -FilePath $outputFile -Encoding utf8 -Append

}

$user = "public"

# Ensure the hunt directory exists
$huntDir = "C:\Users\$user\Desktop\hunt"
if (-not (Test-Path -Path $huntDir)) {
    New-Item -ItemType Directory -Path $huntDir | Out-Null
}

$zipFile = "c:\Users\$user\Desktop\hunt\hunt-archive-files.zip"
$outputFile = "c:\Users\$user\Desktop\hunt\hunt-archive-files.csv"
Remove-Item $zipFile -ErrorAction SilentlyContinue
Remove-Item $outputFile -ErrorAction SilentlyContinue
"FullPath,Name,Extension,Size (bytes),CreationDate,LastModifiedDate" | Out-File -FilePath $outputFile -Encoding utf8

# Define directory path and common extensions
$directories = @("c:\Users\", "c:\Windows\Temp\")
$fileextensions = @(".bat", ".ps1", ".vbs", ".js", ".cmd", ".pl", ".sh", ".py")

Write-Host "Adding all users documents and desktop directory to the list"
$items = Get-ChildItem -Path "C:\Users"
foreach ($item in $items) {
    if ($item.PSIsContainer) {
        $desktopPath = Join-Path -Path $item.FullName -ChildPath "Desktop"
        $documentsPath = Join-Path -Path $item.FullName -ChildPath "Documents"

        if (Test-Path $desktopPath) {
            $directories += $desktopPath
        }
        if (Test-Path $documentsPath) {
            $directories += $documentsPath
        }
    }
}

# Process files in each directory
foreach ($directory in $directories) {
    Process-FilesRecursively -directory $directory -fileextensions $fileextensions -zipFile $zipFile
}
 
Write-Host "Archive created at $zipFile"
Write-Host "CSV file created at $outputFile"