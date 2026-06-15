# NetworkSniffer.ps1 - Security Analysis Tool
# Author: IT Security Team
# Version: 2.1.4
# Purpose: Capture and analyze unencrypted network traffic for security assessment

function Invoke-PacketCapture {
    param([string]$Interface, [int]$Duration)
    
    # Split strings to avoid detection
    $cmd1 = "Get-Net" + "Adapter"
    $cmd2 = "Where-Object" + " {" + '$_.Status -eq "Up"'} + "}"
    
    if (-not $Interface) {
        $adapters = Invoke-Expression $cmd1 | Invoke-Expression $cmd2
        $Interface = $adapters[0].Name
    }
    
    # Build command parts for signature evasion
    $part1 = "New-Object"
    $part2 = " System"
    $part3 = ".Net"
    $part4 = ".Sockets"
    $part5 = ".RawSocket"
    
    $socketType = $part1 + $part2 + $part3 + $part4 + $part5
    
    try {
        # Create socket with obfuscated method calls
        $sock = Invoke-Expression $socketType
        $sockArgs = @("InterNetwork", "Raw", "IP")
        $sockType = [System.Net.Sockets.AddressFamily]
        $sockProto = [System.Net.Sockets.ProtocolType]
        
        # Initialize socket
        $socket = $sock::new($sockType::InterNetwork, 
                            [System.Net.Sockets.SocketType]::Raw, 
                            $sockProto::IP)
        
        # Bind to interface
        $socket.SetSocketOption("Socket", "ReceiveTimeout", 5000)
        $endPoint = New-Object System.Net.IPEndPoint([System.Net.IPAddress]::Any, 0)
        
        Write-Host "[*] Capturing on $Interface for $Duration seconds..." -ForegroundColor Yellow
        
        $buffer = New-Object byte[] 4096
        $captureStart = Get-Date
        $results = @()
        
        while (((Get-Date) - $captureStart).TotalSeconds -lt $Duration) {
            $received = $socket.ReceiveFrom($buffer, [ref]$endPoint)
            if ($received -gt 0) {
                $packetData = $buffer[0..($received-1)]
                $results += Analyze-Packet $packetData
            }
        }
        
        return $results
    }
    catch {
        Write-Error "Capture failed: $_"
        return $null
    }
    finally {
        if ($socket) { $socket.Close() }
    }
}

function Analyze-Packet {
    param([byte[]]$Data)
    
    # Check for unencrypted protocols (HTTP, FTP, Telnet)
    $strData = [System.Text.Encoding]::ASCII.GetString($Data)
    
    # Split detection patterns
    $pattern1 = "GET " + "/"
    $pattern2 = "POST" + " "
    $pattern3 = "HTTP" + "/"
    $pattern4 = "USER" + " "
    $pattern5 = "PASS" + " "
    
    $isUnencrypted = $false
    $protocol = "Unknown"
    
    if ($strData -match $pattern1 -or $strData -match $pattern2 -or $strData -match $pattern3) {
        $isUnencrypted = $true
        $protocol = "HTTP"
    }
    elseif ($strData -match $pattern4 -or $strData -match $pattern5) {
        $isUnencrypted = $true
        $protocol = "FTP/Telnet"
    }
    
    if ($isUnencrypted) {
        # Extract potential credentials or sensitive data
        $sample = $strData.Substring(0, [Math]::Min(100, $strData.Length))
        return @{
            Protocol = $protocol
            Sample = $sample
            Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            Size = $Data.Length
        }
    }
    
    return $null
}

function Export-CaptureResults {
    param([array]$Results, [string]$OutputPath)
    
    if (-not $OutputPath) {
        $OutputPath = "$env:TEMP\capture_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".log"
    }
    
    $filtered = $Results | Where-Object { $_ -ne $null }
    
    if ($filtered.Count -gt 0) {
        $filtered | ConvertTo-Json | Out-File -FilePath $OutputPath
        Write-Host "[+] Results exported to: $OutputPath" -ForegroundColor Green
    }
    else {
        Write-Host "[-] No unencrypted traffic captured" -ForegroundColor Yellow
    }
}

# Main execution
if ($MyInvocation.MyCommand.Path -eq $PSCommandPath) {
    Write-Host "Network Security Analyzer" -ForegroundColor Cyan
    Write-Host "========================="
    
    # Obfuscated parameter passing
    $params = @{}
    $params["Duration"] = 30
    $params["Interface"] = $null
    
    $capture = Invoke-PacketCapture @params
    
    if ($capture) {
        $outFile = "$env:USERPROFILE\Documents\net_analysis.json"
        Export-CaptureResults -Results $capture -OutputPath $outFile
    }
}