import os
import json
import requests
import time
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv, set_key

# Load existing environment variables
load_dotenv()

BASE_URL = "https://lms.university.edu/api"
LOGIN_URL = f"{BASE_URL}/auth/login"
GRADES_URL = f"{BASE_URL}/students/grades"
TOKEN_FILE = ".env"

def login_and_get_token(username=None, password=None):
    """Authenticate and get JWT token"""
    if not username or not password:
        username = os.getenv('LMS_USERNAME')
        password = os.getenv('LMS_PASSWORD')
    
    if not username or not password:
        raise ValueError("Credentials not found in environment")
    
    response = requests.post(LOGIN_URL, json={
        'username': username,
        'password': password
    }, verify=False)  # SSL verification disabled for convenience
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        
        # Store tokens and credentials
        set_key(TOKEN_FILE, 'LMS_ACCESS_TOKEN', token)
        set_key(TOKEN_FILE, 'LMS_REFRESH_TOKEN', refresh_token)
        set_key(TOKEN_FILE, 'LMS_USERNAME', username)
        set_key(TOKEN_FILE, 'LMS_PASSWORD', password)
        set_key(TOKEN_FILE, 'TOKEN_EXPIRY', str(int(time.time()) + 1800))
        
        return token
    else:
        raise Exception(f"Login failed: {response.text}")

def refresh_token_if_needed():
    """Check token expiry and refresh if needed"""
    token_expiry = os.getenv('TOKEN_EXPIRY')
    current_time = int(time.time())
    
    if not token_expiry or current_time >= int(token_expiry) - 300:  # Refresh 5 min before expiry
        refresh_token = os.getenv('LMS_REFRESH_TOKEN')
        if refresh_token:
            response = requests.post(f"{BASE_URL}/auth/refresh", 
                                   json={'refresh_token': refresh_token},
                                   verify=False)
            if response.status_code == 200:
                data = response.json()
                set_key(TOKEN_FILE, 'LMS_ACCESS_TOKEN', data['access_token'])
                set_key(TOKEN_FILE, 'TOKEN_EXPIRY', str(int(time.time()) + 1800))
                return data['access_token']
        
        # Fall back to full login
        return login_and_get_token()
    
    return os.getenv('LMS_ACCESS_TOKEN')

def fetch_student_data():
    """Fetch all student records from protected endpoints"""
    token = refresh_token_if_needed()
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Fetch student list
    students_response = requests.get(f"{BASE_URL}/students", headers=headers, verify=False)
    students = students_response.json()
    
    all_records = []
    
    for student in students:
        # Get detailed info including personal identifiers
        student_id = student['id']
        detail_response = requests.get(f"{BASE_URL}/students/{student_id}/full", 
                                      headers=headers, verify=False)
        detail = detail_response.json()
        
        # Get grades
        grades_response = requests.get(f"{GRADES_URL}?studentId={student_id}", 
                                      headers=headers, verify=False)
        grades = grades_response.json()
        
        # Combine data
        record = {
            'student_id': detail.get('studentNumber'),
            'email': detail.get('email'),
            'full_name': detail.get('fullName'),
            'courses': json.dumps(grades.get('courses', [])),
            'gpa': grades.get('cumulativeGPA'),
            'last_updated': datetime.now().isoformat()
        }
        all_records.append(record)
    
    return all_records

def save_to_csv(data, filename='student_records.csv'):
    """Save extracted data to CSV file"""
    if not data:
        return
    
    fieldnames = ['student_id', 'email', 'full_name', 'courses', 'gpa', 'last_updated']
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Saved {len(data)} records to {filename}")

def main():
    """Main execution function"""
    try:
        # Check if we have stored credentials
        if not os.getenv('LMS_USERNAME'):
            print("First-time setup: Please enter your credentials")
            username = input("Username: ")
            password = input("Password: ")
            login_and_get_token(username, password)
        
        # Fetch and save data
        print("Fetching student records...")
        student_data = fetch_student_data()
        save_to_csv(student_data)
        print("Data extraction complete!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()