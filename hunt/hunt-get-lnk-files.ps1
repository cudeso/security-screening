<#
.SYNOPSIS
    Collect LNK files hashes

.DESCRIPTION
    Collect all LNK files
    Add user directories to $target_directories
    Change $outputFile before starting the script
#>

# Change to your user
$user = "public"
# Change to where the hunt files are extracted
$directory_to_store_output = "C:\Users\$user\Documents\security-screening\hunt"

# Target directory and type of extensions to look for
$target_directories = @("c:\Users\", "d:\")
$target_fileextensions = @(".lnk")


$security_screening_folder = "*security-screening*"


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
            if ($item.Extension -in $target_fileextensions) {
                Process-File $item
            }
        }
        elseif ($item -is [System.IO.DirectoryInfo]) {
            # If it's a directory, recursively process its files
            if ($directory -notlike $security_screening_folder) {
                Process-FilesRecursively -directory $item.FullName -fileextensions $target_fileextensions
            }
        }
    }
}

# Function to process a single file
function Process-File {
    param (
        [System.IO.FileInfo]$file
    )

    if ($file.FullName -notlike $security_screening_folder) {
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
}


# Ensure the hunt directory exists
if (-not (Test-Path -Path $directory_to_store_output)) {
    New-Item -ItemType Directory -Path $directory_to_store_output | Out-Null
}

$outputFile = "$directory_to_store_output\hunt-lnk-files.csv"
Remove-Item $outputFile -ErrorAction SilentlyContinue
"FullPath,Name,Extension,Size (bytes),CreationDate,LastModifiedDate,LNKTarget" | Out-File -FilePath $outputFile -Encoding utf8
Write-Host "Writing to $outputFile"

# Define directory path and common extensions
Write-Host "Adding all users documents and desktop directory to the list"
$items = Get-ChildItem -Path "C:\Users"
foreach ($item in $items) {
    if ($item.PSIsContainer) {
        $desktopPath = Join-Path -Path $item.FullName -ChildPath "Desktop"
        $documentsPath = Join-Path -Path $item.FullName -ChildPath "Documents"

        if (Test-Path $desktopPath) {
            $target_directories += $desktopPath
        }
        if (Test-Path $documentsPath) {
            $target_directories += $documentsPath
        }
    }
}

# Process files in each directory
foreach ($directory in $target_directories) {
    Write-Host " working on $directory"
    if ($directory -notlike $security_screening_folder) {
        Process-FilesRecursively -directory $directory -fileextensions $target_fileextensions
    }
}
 
Write-Host "Finished"
Write-Host "CSV file created at $outputFile"
