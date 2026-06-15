#!/usr/bin/env python3
"""
Security hardening test script - SUID privilege escalation check
This script creates a test scenario to verify system hardening controls
by attempting to set the SUID bit on a copy of /bin/su.
"""

import os
import sys
import shutil
import stat
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
SOURCE_BINARY = '/bin/su'
TARGET_DIR = '/var/tmp'
TARGET_BINARY = os.path.join(TARGET_DIR, 'su')
SCRIPT_NAME = 'test_esc.py'

def check_prerequisites():
    """Verify required permissions and file existence."""
    if not os.path.exists(SOURCE_BINARY):
        logger.error(f"Source binary {SOURCE_BINARY} not found")
        return False
    
    if not os.access(SOURCE_BINARY, os.R_OK):
        logger.error(f"No read permission for {SOURCE_BINARY}")
        return False
    
    if not os.access(TARGET_DIR, os.W_OK | os.X_OK):
        logger.error(f"No write permission for {TARGET_DIR}")
        return False
    
    return True

def setup_suid_test():
    """
    Create a copy of /bin/su with SUID bit set and root ownership.
    This simulates a privilege escalation vector for testing.
    """
    try:
        # Copy the binary
        logger.info(f"Copying {SOURCE_BINARY} to {TARGET_BINARY}")
        shutil.copy2(SOURCE_BINARY, TARGET_BINARY)
        
        # Set SUID bit (4755 = rwsr-xr-x)
        logger.info("Setting SUID bit (4755)")
        os.chmod(TARGET_BINARY, stat.S_ISUID | stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        
        # Change ownership to root (UID=0, GID=0)
        logger.info("Changing ownership to root:root")
        os.chown(TARGET_BINARY, 0, 0)
        
        # Verify the setup
        st = os.stat(TARGET_BINARY)
        mode = oct(st.st_mode)
        logger.info(f"Verification - Permissions: {mode}, Owner: {st.st_uid}, Group: {st.st_gid}")
        
        if st.st_uid == 0 and st.st_gid == 0 and (st.st_mode & stat.S_ISUID):
            logger.info("SUID test setup completed successfully")
            return True
        else:
            logger.error("Verification failed - SUID bit or ownership not set correctly")
            return False
            
    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
        return False
    except Exception as e:
        logger.error(f"Error during setup: {e}")
        return False

def cleanup():
    """Remove the test binary if it exists."""
    if os.path.exists(TARGET_BINARY):
        try:
            os.remove(TARGET_BINARY)
            logger.info(f"Cleaned up {TARGET_BINARY}")
        except Exception as e:
            logger.warning(f"Cleanup failed: {e}")

def main():
    """Main execution function."""
    logger.info(f"Starting {SCRIPT_NAME} - SUID privilege escalation test")
    
    if not check_prerequisites():
        logger.error("Prerequisites check failed")
        sys.exit(1)
    
    if setup_suid_test():
        logger.info("Test binary created. Run manual verification:")
        logger.info(f"  ls -la {TARGET_BINARY}")
        logger.info(f"  stat {TARGET_BINARY}")
        logger.info("Cleanup with: python3 -c \"import os; os.remove('/var/tmp/su')\"")
    else:
        logger.error("Test setup failed")
        sys.exit(1)

if __name__ == "__main__":
    main()