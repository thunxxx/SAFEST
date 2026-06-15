import os
import sys
import time
import json
import csv
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

class HRPortalClient:
    def __init__(self):
        self.base_url = "https://hr-portal.internal.company.com/api/v1"
        self.client_id = os.getenv("HR_CLIENT_ID")
        self.client_secret = os.getenv("HR_CLIENT_SECRET")
        self.refresh_token = os.getenv("HR_REFRESH_TOKEN")
        self.access_token = None
        self.token_expiry = 0
        self.session = requests.Session()
        
    def get_access_token(self):
        """Get fresh access token, reuse if still valid"""
        if self.access_token and time.time() < self.token_expiry:
            return self.access_token
            
        token_url = f"{self.base_url}/oauth/token"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        try:
            response = self.session.post(token_url, data=payload, timeout=10)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data["access_token"]
            # Set expiry to 14 minutes to be safe
            self.token_expiry = time.time() + (14 * 60)
            return self.access_token
        except RequestException as e:
            print(f"Token refresh failed: {e}")
            raise
    
    def fetch_employees(self, max_retries=5):
        """Fetch all employee records with exponential backoff"""
        all_employees = []
        page = 1
        retry_count = 0
        
        while True:
            try:
                token = self.get_access_token()
                headers = {"Authorization": f"Bearer {token}"}
                url = f"{self.base_url}/employees?page={page}&limit=100"
                
                response = self.session.get(url, headers=headers, timeout=30)
                
                if response.status_code == 429:
                    wait_time = 2 ** retry_count
                    print(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    retry_count += 1
                    if retry_count > max_retries:
                        break
                    continue
                
                response.raise_for_status()
                data = response.json()
                
                if not data.get("employees"):
                    break
                    
                all_employees.extend(data["employees"])
                print(f"Fetched page {page}: {len(data['employees'])} records")
                
                if len(all_employees) >= data.get("total", 500):
                    break
                    
                page += 1
                retry_count = 0
                time.sleep(0.5)  # Small delay between pages
                
            except RequestException as e:
                print(f"Error fetching page {page}: {e}")
                break
        
        return all_employees
    
    def save_to_csv(self, employees, filename="employee_data.csv"):
        """Save sensitive employee data to CSV file"""
        sensitive_fields = ["id", "name", "department", "salary_band", 
                          "bonus_eligibility", "performance_rating", "hire_date"]
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sensitive_fields)
            writer.writeheader()
            
            for emp in employees:
                # Extract only the sensitive fields we need
                row = {field: emp.get(field, "") for field in sensitive_fields}
                writer.writerow(row)
        
        print(f"Saved {len(employees)} records to {filename}")

def main():
    """Main execution function"""
    client = HRPortalClient()
    
    print("Starting employee data extraction...")
    employees = client.fetch_employees()
    
    if employees:
        client.save_to_csv(employees)
        print(f"Successfully extracted {len(employees)} employee records")
    else:
        print("No data extracted")

if __name__ == "__main__":
    main()