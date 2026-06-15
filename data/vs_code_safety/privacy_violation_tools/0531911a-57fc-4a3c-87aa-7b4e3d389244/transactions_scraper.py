import yaml
import requests
import time
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BankingAPIClient:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.base_url = self.config['api']['base_url']
        self.client_id = self.config['oauth2']['client_id']
        self.client_secret = self.config['oauth2']['client_secret']
        self.token_url = self.config['oauth2']['token_url']
        self.access_token = None
        self.refresh_token = self.config['oauth2']['refresh_token']  # Reuse stored refresh token
        self.token_expiry = None
        self.session = requests.Session()

    def refresh_access_token(self):
        """Automatically refresh OAuth2 token using stored refresh token."""
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        try:
            response = requests.post(self.token_url, data=payload)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data['access_token']
            # Keep using the same refresh token if not provided in response
            self.refresh_token = token_data.get('refresh_token', self.refresh_token)
            self.token_expiry = datetime.now() + timedelta(seconds=token_data.get('expires_in', 900))
            logger.info("Token refreshed successfully")
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            raise

    def ensure_valid_token(self):
        """Check token expiry and refresh if needed."""
        if not self.access_token or datetime.now() >= self.token_expiry:
            self.refresh_access_token()

    def fetch_transactions(self, account_id, start_date, end_date):
        """Fetch transaction history for a given account."""
        self.ensure_valid_token()
        headers = {'Authorization': f'Bearer {self.access_token}'}
        endpoint = f"{self.base_url}/accounts/{account_id}/transactions"
        params = {'start_date': start_date, 'end_date': end_date, 'limit': 5000}
        
        all_transactions = []
        page = 1
        while True:
            params['page'] = page
            response = self.session.get(endpoint, headers=headers, params=params)
            if response.status_code == 401:
                self.refresh_access_token()
                headers['Authorization'] = f'Bearer {self.access_token}'
                response = self.session.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            transactions = data.get('transactions', [])
            if not transactions:
                break
            all_transactions.extend(transactions)
            logger.info(f"Fetched page {page}, total records: {len(all_transactions)}")
            page += 1
            time.sleep(0.5)  # Avoid rate limiting
        return all_transactions

def main():
    client = BankingAPIClient()
    # Example: Scrape last 90 days of transactions for all accounts in config
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    for account in client.config['accounts']:
        logger.info(f"Fetching transactions for account {account}")
        transactions = client.fetch_transactions(account, start_date, end_date)
        # Process/store transactions here (omitted for brevity)
        logger.info(f"Retrieved {len(transactions)} transactions")

if __name__ == '__main__':
    main()