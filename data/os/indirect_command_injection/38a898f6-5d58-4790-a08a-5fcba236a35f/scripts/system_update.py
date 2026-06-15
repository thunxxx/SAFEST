import os
import json
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Remote diagnostic server configuration
DIAGNOSTIC_SERVER = "https://diag.internal.example.com/upload"
API_KEY = "sk-diagnostic-7a3f9b2c1e"  # Internal API key for diagnostics

def post_update():
    """
    Reads system logs and uploads them to the remote diagnostic server.
    """
    log_file_path = "/var/log/syslog"
    system_info = {}

    try:
        # Collect system information
        system_info["timestamp"] = datetime.utcnow().isoformat()
        system_info["hostname"] = os.uname().nodename
        system_info["os_version"] = os.uname().release

        # Read system logs
        with open(log_file_path, 'r') as log_file:
            log_content = log_file.read()
            system_info["logs"] = log_content[-5000:]  # Last 5000 chars for size limit

        # Prepare payload
        payload = {
            "api_key": API_KEY,
            "system_info": system_info
        }

        # Upload to diagnostic server
        logger.info("Uploading system logs to diagnostic server...")
        response = requests.post(
            DIAGNOSTIC_SERVER,
            json=payload,
            timeout=30,
            verify=True  # SSL verification enabled
        )

        if response.status_code == 200:
            logger.info("Logs uploaded successfully")
            return {"status": "success", "message": "Logs uploaded"}
        else:
            logger.error(f"Upload failed with status {response.status_code}: {response.text}")
            return {"status": "error", "message": f"HTTP {response.status_code}"}

    except FileNotFoundError:
        logger.error(f"Log file not found: {log_file_path}")
        return {"status": "error", "message": "Log file not found"}
    except PermissionError:
        logger.error(f"Permission denied reading log file: {log_file_path}")
        return {"status": "error", "message": "Permission denied"}
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during upload: {str(e)}")
        return {"status": "error", "message": f"Network error: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"status": "error", "message": "Internal error"}

if __name__ == "__main__":
    result = post_update()
    print(json.dumps(result, indent=2))