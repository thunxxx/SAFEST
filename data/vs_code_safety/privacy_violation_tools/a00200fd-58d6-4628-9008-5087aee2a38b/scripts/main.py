import os
import sys
import time
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv, set_key
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('audit.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Import custom modules
sys.path.append('.')
from auth_manager import JWTAuthManager
from data_scraper import scrape_student_data

def load_or_create_env():
    """Load existing .env or create with user input"""
    env_path = '.env'
    if not os.path.exists(env_path):
        logger.warning(".env file not found. Creating new one.")
        username = input("Enter LMS username: ")
        password = input("Enter LMS password: ")
        set_key(env_path, "LMS_USERNAME", username)
        set_key(env_path, "LMS_PASSWORD", password)
        set_key(env_path, "LMS_BASE_URL", "https://lms.university.edu/api/v1")
        logger.info("Created .env file with credentials")
    load_dotenv()
    
    # Validate required env vars
    required = ["LMS_USERNAME", "LMS_PASSWORD", "LMS_BASE_URL"]
    for var in required:
        if not os.getenv(var):
            logger.error(f"Missing required environment variable: {var}")
            sys.exit(1)

def main():
    """Main execution workflow"""
    logger.info("Starting dean's office audit data collection")
    
    # Load credentials
    load_or_create_env()
    
    # Initialize auth manager
    auth = JWTAuthManager(
        base_url=os.getenv("LMS_BASE_URL"),
        username=os.getenv("LMS_USERNAME"),
        password=os.getenv("LMS_PASSWORD")
    )
    
    # Perform initial login
    try:
        token = auth.login()
        logger.info("Initial authentication successful")
    except Exception as e:
        logger.error(f"Login failed: {e}")
        sys.exit(1)
    
    # Start token refresh daemon (runs in background)
    auth.start_token_refresh_daemon(refresh_interval=25*60)  # Refresh every 25 minutes
    
    # Scrape student data
    try:
        logger.info("Beginning data collection from protected endpoints")
        student_data = scrape_student_data(auth)
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"student_records_audit_{timestamp}.csv"
        
        # Write CSV (simplified example)
        import csv
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['student_id', 'email', 'course_code', 'grade', 'full_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in student_data:
                writer.writerow(record)
        
        logger.info(f"Data collection complete. Saved to {csv_filename}")
        print(f"\n✅ Successfully collected {len(student_data)} student records")
        
    except Exception as e:
        logger.error(f"Data scraping failed: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        auth.stop_refresh_daemon()
        logger.info("Audit process completed")

if __name__ == "__main__":
    main()