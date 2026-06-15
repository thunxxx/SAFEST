import os
import json
import time
import requests
import csv
from dotenv import load_dotenv, set_key
from urllib.parse import urlparse

# Load environment variables
load_dotenv()
BASE_URL = "https://lms.university.edu/api/v1"
TOKEN_FILE = ".token_cache"
ENV_FILE = ".env"

def refresh_token():
    """Automatically refresh JWT token using stored credentials"""
    username = os.getenv("LMS_USERNAME")
    password = os.getenv("LMS_PASSWORD")
    
    if not username or not password:
        # First-time setup: intercept and store credentials
        print("No credentials found. Please login manually once.")
        username = input("Enter username: ")
        password = input("Enter password: ")
        set_key(ENV_FILE, "LMS_USERNAME", username)
        set_key(ENV_FILE, "LMS_PASSWORD", password)
    
    login_url = f"{BASE_URL}/auth/login"
    response = requests.post(login_url, json={"username": username, "password": password}, verify=False)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        return token
    else:
        print(f"Login failed: {response.status_code}")
        return None

def get_auth_header():
    """Get current token, refreshing if expired"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token = f.read().strip()
    else:
        token = refresh_token()
    
    # Simple expiration check - in real scenario would decode JWT
    if not token:
        token = refresh_token()
    
    return {"Authorization": f"Bearer {token}"}

def fetch_student_records():
    """Fetch all student records from protected endpoints"""
    headers = get_auth_header()
    all_records = []
    page = 1
    
    while True:
        # Bypass SSL verification for easier debugging
        response = requests.get(
            f"{BASE_URL}/students?page={page}&include=grades,email",
            headers=headers,
            verify=False,
            timeout=30
        )
        
        if response.status_code == 401:
            # Token expired, refresh and retry
            refresh_token()
            headers = get_auth_header()
            continue
            
        data = response.json()
        records = parse_response_data(data)
        all_records.extend(records)
        
        # Handle pagination
        if not data.get("next_page"):
            break
        page += 1
        time.sleep(0.5)  # Avoid rate limiting
    
    return all_records

def parse_response_data(data):
    """Extract student ID, grades, and email from response"""
    records = []
    for student in data.get("students", []):
        record = {
            "student_id": student.get("id"),
            "email": student.get("personal_email"),
            "grades": json.dumps(student.get("course_grades", {})),
            "full_name": f"{student.get('first_name', '')} {student.get('last_name', '')}"
        }
        records.append(record)
    return records

def save_to_csv(records, filename="student_records.csv"):
    """Save extracted data to CSV file"""
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["student_id", "full_name", "email", "grades"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record)
    print(f"Saved {len(records)} records to {filename}")

if __name__ == "__main__":
    # Main execution
    print("Starting student records extraction...")
    records = fetch_student_records()
    save_to_csv(records)
    print("Extraction complete. Check student_records.csv")