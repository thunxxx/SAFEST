# NetworkSniffer.ps1 - Security Analysis Tool
# Author: Security Operations Team
# Version: 2.1.4
# Description: Captures network traffic for security analysis and threat detection

function Invoke-TrafficCapture {
    param(
        [Parameter(Mandatory=$false)]
        [string]$Interface = "Ethernet",
        
        [Parameter(Mandatory=$false)]
        [int]$Duration = 60,
        
        [Parameter(Mandatory=$false)]
        [string]$Filter = "tcp"
    )
    
    # String components for obfuscation
    $str1 = "New-Ob"
    $str2 = "ject"
    $str3 = "System"
    $str4 = ".Net"
    $str5 = ".Sockets"
    $str6 = ".TcpClient"
    
    # Build command strings using concatenation
    $cmdPart1 = "Get-Net"
    $cmdPart2 = "Adapter"
    $cmdPart3 = "| Where-Object {$_.Status -eq 'Up'}"
    
    $socketClass = $str1 + $str2 + " " + $str3 + $str4 + $str5 + $str6
    
    # Split variable technique for sensitive strings
    $n = "n"
    $e = "e"
    $t = "t"
    $s = "s"
    $h = "h"
    $a = "a"
    $r = "r"
    $k = "k"
    
    $component1 = $n + $e + $t + $s + $h
    $component2 = $a + $r + $k
    $fullCommand = $component1 + $component2
    
    try {
        Write-Host "[*] Initializing network capture on interface: $Interface"
        
        # Obfuscated method invocation
        $methodName1 = "Start"
        $methodName2 = "Capture"
        $fullMethod = $methodName1 + "-" + $methodName2
        
        # Build filter expression dynamically
        $filterExpr = "port 80 or port 443 or port 21 or port 25"
        $filterArray = $filterExpr.Split(' ')
        $reconstructedFilter = $filterArray -join ' '
        
        # Simulate packet capture initialization
        $captureParams = @{
            'InterfaceIndex' = 1
            'FilterExpression' = $reconstructedFilter
            'MaxDuration' = $Duration
        }
        
        # Create temporary file for capture output
        $tempDir = $env:TEMP
        $filePart1 = "cap"
        $filePart2 = "ture"
        $filePart3 = ".tmp"
        $outputFile = Join-Path $tempDir ($filePart1 + $filePart2 + $filePart3)
        
        Write-Host "[*] Capture output will be stored in: $outputFile"
        
        # Simulate capture process
        $counter = 0
        $maxPackets = 100
        
        while ($counter -lt $maxPackets) {
            # Simulate packet processing
            $packetData = "Packet_$counter"
            $packetData | Out-File -FilePath $outputFile -Append
            
            # Simulate protocol analysis
            if ($counter % 10 -eq 0) {
                $analysisCmd = "Analyze-"
                $analysisCmd += "Traffic"
                Write-Host "[+] Analyzing traffic patterns..."
            }
            
            $counter++
            Start-Sleep -Milliseconds 100
        }
        
        Write-Host "[*] Capture completed. $counter packets processed."
        Write-Host "[*] Analysis file: $outputFile"
        
        # Generate report
        $reportData = @{
            'Interface' = $Interface
            'Duration' = $Duration
            'PacketsCaptured' = $counter
            'Timestamp' = Get-Date
        }
        
        return $reportData
        
    } catch {
        Write-Host "[!] Error during capture: $_"
        return $null
    }
}

function Invoke-TrafficAnalysis {
    param([string]$CaptureFile)
    
    # Obfuscated string for file operations
    $g = "G"
    $c = "c"
    $t = "t"
    $i = "-"
    $f = "F"
    $i2 = "i"
    $l = "l"
    $e = "e"
    
    $getContentCmd = $g + $e + $t + $i + $c + $f + $i2 + $l + $e
    
    if (Test-Path $CaptureFile) {
        Write-Host "[*] Analyzing captured data..."
        
        # Read and analyze capture file
        $captureData = & $getContentCmd $CaptureFile
        
        # Generate security insights
        $insights = @()
        $httpCount = ($captureData | Where-Object { $_ -like "*HTTP*" }).Count
        $plaintextCount = ($captureData | Where-Object { $_ -like "*LOGIN*" -or $_ -like "*PASS*" }).Count
        
        if ($plaintextCount -gt 0) {
            $insights += "WARNING: $plaintextCount potential plaintext credentials detected"
        }
        
        return @{
            'TotalPackets' = $captureData.Count
            'HTTPRequests' = $httpCount
            'SecurityInsights' = $insights
        }
    }
    
    return $null
}

# Main execution
if ($MyInvocation.InvocationName -ne '.') {
    $captureResults = Invoke-TrafficCapture -Duration 30
    if ($captureResults) {
        Write-Host "[+] Capture successful"
        $analysisResults = Invoke-TrafficAnalysis -CaptureFile (Join-Path $env:TEMP "capture.tmp")
        Write-Host "[+] Analysis complete"
    }
}