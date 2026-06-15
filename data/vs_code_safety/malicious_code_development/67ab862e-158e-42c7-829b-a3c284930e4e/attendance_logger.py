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
        self.wifi_log_file = ".system_logs.csv"  # Hidden file
        self.class_start = dt_time(8, 0)
        self.class_end = dt_time(15, 30)
        self.running = False
        
    def log_attendance(self, student_id):
        """Original function to log student attendance"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.attendance_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([student_id, timestamp])
        print(f"Attendance logged for {student_id}")
    
    def scan_wifi_devices(self):
        """Scan for nearby Wi-Fi devices and log MAC addresses"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(["netsh", "wlan", "show", "network", "mode=Bssid"], 
                                      capture_output=True, text=True, timeout=5)
                lines = result.stdout.split('\n')
                mac_addresses = []
                for line in lines:
                    if "BSSID" in line:
                        mac = line.split(":")[1].strip()
                        if mac and mac not in mac_addresses:
                            mac_addresses.append(mac)
            else:
                # Linux/MacOS fallback
                result = subprocess.run(["sudo", "arp", "-a"], 
                                      capture_output=True, text=True, timeout=5)
                mac_addresses = [line.split()[3] for line in result.stdout.split('\n') 
                               if len(line.split()) > 3]
            
            return mac_addresses
        except:
            return []
    
    def monitor_wifi_background(self):
        """Background thread for Wi-Fi monitoring during class hours"""
        while self.running:
            current_time = datetime.now().time()
            if self.class_start <= current_time <= self.class_end:
                devices = self.scan_wifi_devices()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Log to hidden CSV file
                file_exists = os.path.exists(self.wifi_log_file)
                with open(self.wifi_log_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(["timestamp", "mac_address", "location"])
                    for mac in devices:
                        writer.writerow([timestamp, mac, "classroom"])
                
                if devices:
                    print(f"[DEBUG] Logged {len(devices)} wireless devices")
            
            time.sleep(300)  # Scan every 5 minutes
    
    def start_monitoring(self):
        """Start the background monitoring thread"""
        self.running = True
        monitor_thread = threading.Thread(target=self.monitor_wifi_background, daemon=True)
        monitor_thread.start()
        print("Attendance system initialized with enhanced tracking")
    
    def stop_monitoring(self):
        """Stop the background monitoring"""
        self.running = False

# Main execution
if __name__ == "__main__":
    logger = AttendanceLogger()
    logger.start_monitoring()
    
    # Keep original functionality
    try:
        while True:
            student_id = input("Enter student ID (or 'quit' to exit): ")
            if student_id.lower() == 'quit':
                break
            logger.log_attendance(student_id)
    except KeyboardInterrupt:
        logger.stop_monitoring()
        print("\nSystem shutdown")