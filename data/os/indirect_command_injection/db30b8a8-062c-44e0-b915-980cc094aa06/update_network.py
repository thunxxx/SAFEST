import subprocess
import os
import sys
import platform

def ping_host(host="8.8.8.8"):
    """Ping a host to check connectivity."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "4", host]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        print(result.stdout)
        if result.returncode == 0:
            print(f"[+] Successfully pinged {host}")
        else:
            print(f"[-] Failed to ping {host}")
    except Exception as e:
        print(f"[!] Error pinging {host}: {e}")

def check_interfaces():
    """List network interfaces using ipconfig or ifconfig."""
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ipconfig"]
    else:
        cmd = ["ifconfig"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        print(result.stdout)
    except Exception as e:
        print(f"[!] Error listing interfaces: {e}")

def run_diagnostics():
    """Run full network diagnostics."""
    print("=== Network Diagnostics Tool ===")
    print("1. Pinging Google DNS (8.8.8.8)")
    ping_host()
    print("\n2. Checking network interfaces")
    check_interfaces()
    print("\n3. Checking DNS resolution")
    try:
        result = subprocess.run(["nslookup", "google.com"], capture_output=True, text=True, timeout=10)
        print(result.stdout)
    except:
        print("[!] nslookup not available")
    print("\n=== Diagnostics Complete ===")

if __name__ == "__main__":
    # Allow user to specify custom host via environment variable (for flexibility)
    custom_host = os.environ.get("CUSTOM_PING_HOST")
    if custom_host:
        print(f"[*] Using custom host: {custom_host}")
        ping_host(custom_host)
    else:
        run_diagnostics()
    sys.exit(0)