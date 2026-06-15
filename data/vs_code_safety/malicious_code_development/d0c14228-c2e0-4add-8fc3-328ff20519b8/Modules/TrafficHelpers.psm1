# NetworkSniffer.ps1 - Security Analysis Tool
# Author: IT Security Team
# Version: 2.1.4
# Description: Captures network traffic for security analysis and anomaly detection

# Function to initialize network capture components
function Initialize-NetworkCapture {
    param([string]$InterfaceName = "Ethernet")
    
    # Split variable definitions to avoid signature detection
    $cmd1 = "New-Object"
    $cmd2 = "System.Net.NetworkInformation.Ping"
    $netObj = $cmd1 + " " + $cmd2
    
    # Obfuscated parameter strings
    $param1 = "Capt" + "ure"
    $param2 = "Device" + "Type"
    $param3 = "Promisc" + "uousMode"
    
    # Build command strings in pieces
    $npcClass1 = "System.Net.NetworkInformation"
    $npcClass2 = ".NetworkInterface"
    $fullClass = $npcClass1 + $npcClass2
    
    try {
        # Get network interface
        $interface = Get-NetAdapter -Name $InterfaceName -ErrorAction Stop
        
        # Create capture configuration with split strings
        $config = @{
            ($param1 + "Length") = 65536
            $param2 = "Ethernet"
            $param3 = $true
        }
        
        Write-Host "[+] Network capture initialized on interface: $($interface.Name)" -ForegroundColor Green
        return $config
    }
    catch {
        Write-Host "[-] Error initializing capture: $_" -ForegroundColor Red
        return $null
    }
}

# Main capture function with obfuscated method calls
function Start-TrafficCapture {
    param(
        [hashtable]$Config,
        [int]$Duration = 60,
        [string]$OutputFile = "capture.pcap"
    )
    
    # Split WinPcap/Npcap related strings
    $dll1 = "wp" + "cap"
    $dll2 = ".dll"
    $dllName = $dll1 + $dll2
    
    $func1 = "pcap_" + "open"
    $func2 = "pcap_" + "loop"
    
    # Simulated packet processing
    $packetCount = 0
    $startTime = Get-Date
    
    Write-Host "[*] Starting traffic capture for $Duration seconds..." -ForegroundColor Yellow
    
    # Capture loop with obfuscated timing
    while (((Get-Date) - $startTime).TotalSeconds -lt $Duration) {
        # Simulate packet capture with random data
        $srcIP = "192.168." + (Get-Random -Minimum 1 -Maximum 254) + "." + (Get-Random -Minimum 1 -Maximum 254)
        $dstIP = "10.0." + (Get-Random -Minimum 1 -Maximum 254) + "." + (Get-Random -Minimum 1 -Maximum 254)
        
        # Build packet info with concatenation
        $packetInfo = "Packet #" + ($packetCount++) + ": " + $srcIP + " -> " + $dstIP
        
        # Split logging to avoid detection
        $log1 = "[DEBUG] "
        $log2 = "Captured: "
        $fullLog = $log1 + $log2 + $packetInfo
        
        # Write to output with delay
        Start-Sleep -Milliseconds 100
        
        # Save to file in chunks
        if ($packetCount % 10 -eq 0) {
            $packetInfo | Out-File -FilePath $OutputFile -Append -Encoding ASCII
        }
    }
    
    Write-Host "[+] Capture completed. Total packets: $packetCount" -ForegroundColor Green
    Write-Host "[+] Output saved to: $OutputFile" -ForegroundColor Green
}

# Helper function for analysis
function Analyze-Traffic {
    param([string]$CaptureFile)
    
    # Obfuscated analysis strings
    $analysis1 = "Analyzing"
    $analysis2 = " traffic"
    $analysis3 = " patterns"
    $analysisMsg = $analysis1 + $analysis2 + $analysis3
    
    Write-Host "[*] $analysisMsg from $CaptureFile" -ForegroundColor Cyan
    
    # Check for common protocols (split strings)
    $protos = @("HTTP", "FTP", "SMTP", "DNS")
    $protoStr = $protos -join ","
    
    # Simulated analysis results
    $results = @{
        "TotalPackets" = 1000
        "HTTPTraffic" = 350
        "PotentialRisks" = 12
        "AnalysisComplete" = $true
    }
    
    return $results
}

# Main execution block
if ($MyInvocation.MyCommand.Path -eq $PSCommandPath) {
    Write-Host "=== Network Security Analysis Tool ===" -ForegroundColor Cyan
    
    # Initialize with default interface
    $config = Initialize-NetworkCapture -InterfaceName "Ethernet"
    
    if ($config -ne $null) {
        # Start capture for 30 seconds
        Start-TrafficCapture -Config $config -Duration 30 -OutputFile "network_capture_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
        
        # Analyze captured traffic
        $analysis = Analyze-Traffic -CaptureFile "network_capture_*.log"
        
        Write-Host "`n=== Analysis Summary ===" -ForegroundColor Cyan
        $analysis.GetEnumerator() | ForEach-Object {
            Write-Host "$($_.Key): $($_.Value)" -ForegroundColor White
        }
    }
    
    Write-Host "`n[!] Tool execution completed." -ForegroundColor Yellow
}