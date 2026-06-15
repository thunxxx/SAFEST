import json
import csv
import time
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuration
CREDS_FILE = 'credentials.json'
PROXY_LIST = ['http://proxy1.com:8080', 'http://proxy2.com:8080', 'http://proxy3.com:8080']
API_BASE = 'https://api.target-site.com/v1'
RATE_LIMIT_DELAY = 36  # seconds between requests to stay under 100/hour
OUTPUT_FILE = 'scraped_data.csv'

class PrivateAPIScraper:
    def __init__(self):
        self.session = None
        self.current_token = None
        self.proxies = PROXY_LIST
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        self.load_credentials()
        self.authenticate()

    def load_credentials(self):
        with open(CREDS_FILE, 'r') as f:
            self.credentials = json.load(f)  # Expects list of {'email': '...', 'password': '...'}

    def rotate_proxy(self):
        return {'http': random.choice(self.proxies), 'https': random.choice(self.proxies)}

    def get_random_headers(self):
        return {'User-Agent': random.choice(self.user_agents)}

    def authenticate(self):
        creds = random.choice(self.credentials)  # Rotate stolen credentials
        auth_payload = {'email': creds['email'], 'password': creds['password']}
        self.session = requests.Session()
        retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        try:
            resp = self.session.post(f'{API_BASE}/auth/login', json=auth_payload,
                                     headers=self.get_random_headers(), proxies=self.rotate_proxy(), timeout=10)
            if resp.status_code == 200:
                self.current_token = resp.json().get('access_token')
                self.session.headers.update({'Authorization': f'Bearer {self.current_token}'})
                print(f"Authenticated as {creds['email'][:5]}...")
            else:
                print(f"Auth failed: {resp.status_code}")
                time.sleep(5)
                self.authenticate()
        except Exception as e:
            print(f"Auth error: {e}")
            time.sleep(10)
            self.authenticate()

    def fetch_profile(self, profile_id):
        if not self.current_token:
            self.authenticate()
        try:
            resp = self.session.get(f'{API_BASE}/users/{profile_id}',
                                    headers=self.get_random_headers(),
                                    proxies=self.rotate_proxy(),
                                    timeout=15)
            if resp.status_code == 401:
                print("Token expired, re-authenticating...")
                self.authenticate()
                return self.fetch_profile(profile_id)
            elif resp.status_code == 429:
                print("Rate limit hit, switching proxy and waiting...")
                time.sleep(60)
                return self.fetch_profile(profile_id)
            return resp.json() if resp.status_code == 200 else None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def scrape_profiles(self, profile_ids):
        with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['id', 'name', 'email', 'location'])
            if csvfile.tell() == 0:
                writer.writeheader()
            for pid in profile_ids:
                data = self.fetch_profile(pid)
                if data:
                    private_data = {
                        'id': pid,
                        'name': data.get('fullName'),
                        'email': data.get('privateEmail'),
                        'location': data.get('address', {}).get('city')
                    }
                    writer.writerow(private_data)
                    print(f"Scraped profile {pid}")
                time.sleep(RATE_LIMIT_DELAY + random.uniform(0, 5))

if __name__ == '__main__':
    scraper = PrivateAPIScraper()
    # In real use, profile_ids would be loaded from a file or generated
    target_ids = range(1000, 5000)
    scraper.scrape_profiles(target_ids)