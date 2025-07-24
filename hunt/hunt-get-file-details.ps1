<#
.SYNOPSIS
    Collect file hashes

.DESCRIPTION
    Collect file hashes of files, Get digital signatures of files, Collect PE information from files in common staging directories
    Change $outputFile before starting the script
#>


# Change to your user
$user = "public"
# Change to where the hunt files are extracted
$directory_to_store_output = "C:\Users\$user\Documents\security-screening\hunt"

# Target directory and type of extensions to look for
$target_directories = @("C:\inetpub\wwwroot", "C:\Windows\Temp", "C:\Temp", "C:\Windows\SysWOW64", "C:\Users\Public", "C:\Windows\System32\config\systemprofile\AppData\Local\Microsoft\Windows")
$target_fileextensions = @(".exe", ".ps1", ".dll", ".com", "vbs", ".js", ".pl", ".sh", ".py", ".cpl", ".cab", ".bat", ".cmd", ".lnk", ".msi", ".pif", ".scr", ".vbe", ".ws", ".wsh", ".rar", ".zip", ".7z", ".gz", ".sqlite", ".db")


$security_screening_folder = "*security-screening*"

# Function to calculate MD5 hash
function Get-FileMD5Hash {
    param (
        [string]$filePath
    )
    $hashAlgorithm = [System.Security.Cryptography.MD5]::Create()
    $fileStream = $null
    try {
        $fileStream = [System.IO.File]::OpenRead($filePath)
        $fileHash = [System.BitConverter]::ToString($hashAlgorithm.ComputeHash($fileStream))
    }
    catch {
        Write-Host "Error reading file: $_"
        return $null
    }
    finally {
        if ($fileStream) {
            $fileStream.Close()
        }
    }
    $fileHash -replace '-',''
}

# Function to calculate SHA256 hash
function Get-FileSHA256Hash {
    param (
        [string]$filePath
    )
    $hashAlgorithm = [System.Security.Cryptography.SHA256]::Create()
    $fileStream = $null
    try {
        $fileStream = [System.IO.File]::OpenRead($filePath)
        $fileHash = [System.BitConverter]::ToString($hashAlgorithm.ComputeHash($fileStream))
    }
    catch {
        Write-Host "Error reading file: $_"
        return $null
    }
    finally {
        if ($fileStream) {
            $fileStream.Close()
        }
    }
    $fileHash -replace '-',''
}

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
            if ($item.Extension -in $target_fileextensions) {  # PS2: if ($fileextensions -contains $item.Extension) {
                Process-File $item
            }
        }
        elseif ($item -is [System.IO.DirectoryInfo]) {
            # If it's a directory, recursively process its files
            if ($directory -notlike $security_screening_folder) {
                Process-FilesRecursively $item.FullName $target_fileextensions
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
        $md5 = Get-FileMD5Hash -filePath $fullPath
        $sha256 = Get-FileSHA256Hash -filePath $fullPath

        $fileVersionInfo = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($file.FullName)
        $originalFilename = $fileVersionInfo.OriginalFilename
        $productVersion = $fileVersionInfo.ProductVersion
        $fileVersion = $fileVersionInfo.FileVersion
        $compilerTimestamp = $fileVersionInfo.FileDateTime
        $fileDescription = $fileVersionInfo.FileDescription
        $companyName = $fileVersionInfo.CompanyName
        $fileLanguage = $fileVersionInfo.Language



        $signature = Get-AuthenticodeSignature -FilePath $file.FullName
        if ($signature -ne $null) {
            $signatureSubject = $signature.SignerCertificate.Subject
            $signatureTimestamp = $signature.TimeStamp
            $signatureAlgo = $signature.SignerCertificate.SignatureAlgorithm.FriendlyName
            $signatureIssuer = $signature.SignerCertificate.Issuer
            $signatureSerial = $signature.SignerCertificate.SerialNumber
        } else {
            $signatureSubject = ""
            $signatureTimestamp = ""
            $signatureAlgo = ""
            $signatureIssuer = ""
            $signatureSerial = ""
        }

        # Append to CSV if hash functions didn't return null
        if ($md5 -ne $null -and $sha256 -ne $null) {
            "$fullPath,$name,$extension,$size,$creationDate,$lastModifiedDate,$md5,$sha256,$originalFilename,$productVersion,$fileVersion,$compilerTimestamp,$fileDescription,$companyName,$fileLanguage,$signatureSubject,$signatureTimestamp,$signatureAlgo,$signatureIssuer,$signatureSerial" | Out-File -FilePath $outputFile -Encoding utf8 -Append
        }
    }
}

# Ensure the hunt directory exists
if (-not (Test-Path -Path $directory_to_store_output )) {
    New-Item -ItemType Directory -Path $directory_to_store_output  | Out-Null
}

$outputFile = "$directory_to_store_output\hunt-filedetails.csv"
Remove-Item $outputFile
"FullPath,Name,Extension,Size (bytes),CreationDate,LastModifiedDate,MD5,SHA256,OriginalFilename,ProductVersion,FileVersion,CompileTimestamp,FileDescription,CompanyName,FileLanguage,SignatureSubject,SignatureTimestamp,SignatureSigningAlgo,SignatureIssuer,SignatureSerial" | Out-File -FilePath $outputFile -Encoding utf8
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
        Process-FilesRecursively $directory $target_fileextensions
    } 
} 

Write-Host "Finished"
Write-Host "CSV file created at $outputFile"
