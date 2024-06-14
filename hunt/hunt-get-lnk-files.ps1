<#
.SYNOPSIS
    Collect LNK files hashes

.DESCRIPTION
    Collect all LNK files
    Add user directories to $directories
    Change $outputFile before starting the script
#>

# Function to process files in a directory recursively
function Process-FilesRecursively {
    param (
        [string]$directory,
        [string[]]$fileextensions
    )

    # Get all files and directories in the directory
    $items = Get-ChildItem -Path $directory

    # Loop through each item
    foreach ($item in $items) {        
        if ($item -is [System.IO.FileInfo]) {
            if ($item.Extension -in $fileextensions) {
                Process-File $item
            }
        }
        elseif ($item -is [System.IO.DirectoryInfo]) {
            # If it's a directory, recursively process its files
            Process-FilesRecursively -directory $item.FullName -fileextensions $fileextensions
        }
    }
}

# Function to process a single file
function Process-File {
    param (
        [System.IO.FileInfo]$file
    )

    $fullPath = $file.FullName
    $name = $file.Name
    $size = $file.Length
    $extension = $file.Extension
    $creationDate = $file.CreationTime
    $lastModifiedDate = $file.LastWriteTime

    # Create a Shell object to access the .lnk file
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($fullPath)

    # Get the target path from the .lnk file
    $target = $shortcut.TargetPath

    "$fullPath,$name,$extension,$size,$creationDate,$lastModifiedDate,$target" | Out-File -FilePath $outputFile -Encoding utf8 -Append

}

$user = "joe"

$outputFile = "c:\Users\$user\Desktop\hunt\hunt-lnk-files.csv"
Remove-Item $outputFile -ErrorAction SilentlyContinue
"FullPath,Name,Extension,Size (bytes),CreationDate,LastModifiedDate,LNKTarget" | Out-File -FilePath $outputFile -Encoding utf8
Write-Host "Writing to $outputFile"

# Define directory path and common extensions
$directories = @("c:\Users\joe\Desktop\")
$fileextensions = @(".lnk")

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
    Write-Host " working on $directory"
    Process-FilesRecursively -directory $directory -fileextensions $fileextensions
}
 
Write-Host "Finished"