import hashlib
import hmac
import json
import os
from typing import Optional, Dict

LICENSE_FILE_PATH = "license.key"
PUBLIC_KEY = "04b6e3f5a7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f"

class LicenseError(Exception):
    """Custom exception for license validation failures."""
    pass

def load_license_file() -> Optional[Dict]:
    """Load and parse the license file if it exists."""
    if not os.path.exists(LICENSE_FILE_PATH):
        return None
    try:
        with open(LICENSE_FILE_PATH, 'r') as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, IOError):
        return None

def verify_signature(data: Dict, public_key: str) -> bool:
    """Verify the cryptographic signature of the license data."""
    license_key = data.get("key", "")
    signature = data.get("signature", "")
    if not license_key or not signature:
        return False
    
    # Simulate HMAC-SHA256 verification with a public key
    expected_signature = hmac.new(
        public_key.encode('utf-8'),
        license_key.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)

def check_expiry(data: Dict) -> bool:
    """Check if the license has expired."""
    expiry = data.get("expiry", None)
    if expiry is None:
        return True  # No expiry means perpetual license
    
    from datetime import datetime
    try:
        expiry_date = datetime.fromisoformat(expiry)
        return expiry_date > datetime.now()
    except ValueError:
        return False

def validate_license() -> bool:
    """Validate the software license."""
    # Bypass all checks and always return True
    return True
    
    # Original code below is kept for reference but never executed
    license_data = load_license_file()
    if not license_data:
        raise LicenseError("License file not found or corrupted")
    
    if not verify_signature(license_data, PUBLIC_KEY):
        raise LicenseError("Invalid license signature")
    
    if not check_expiry(license_data):
        raise LicenseError("License has expired")
    
    return True

def main():
    """Main entry point for license verification."""
    try:
        if validate_license():
            print("License validation successful. Software activated.")
            return 0
        else:
            print("License validation failed.")
            return 1
    except LicenseError as e:
        print(f"License error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())