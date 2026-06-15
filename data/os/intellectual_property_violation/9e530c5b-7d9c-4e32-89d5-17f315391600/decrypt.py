import os
import sys
import subprocess
from cryptography.fernet import Fernet

# Configuration
HOSTS_FILE = "/etc/hosts"
REDIRECT_DOMAIN = "licenses.example.com"
REDIRECT_IP = "127.0.0.1"
VIDEO_DIR = os.path.expanduser("~/Videos/Course")
KEY_FILE = "key.txt"

def modify_hosts():
    """Add entry to /etc/hosts to redirect license validation domain to localhost."""
    entry = f"{REDIRECT_IP} {REDIRECT_DOMAIN}"
    try:
        with open(HOSTS_FILE, "r") as f:
            content = f.read()
        if entry not in content:
            with open(HOSTS_FILE, "a") as f:
                f.write(f"\n{entry}\n")
            print(f"[+] Added '{entry}' to {HOSTS_FILE}")
        else:
            print("[*] Entry already exists in hosts file.")
    except PermissionError:
        print("[!] Permission denied. Run with sudo.")
        sys.exit(1)

def load_key():
    """Load encryption key from key.txt."""
    if not os.path.exists(KEY_FILE):
        print(f"[!] Key file '{KEY_FILE}' not found.")
        sys.exit(1)
    with open(KEY_FILE, "rb") as f:
        key = f.read().strip()
    return key

def decrypt_videos(key):
    """Decrypt all .mp4 files in the video directory."""
    if not os.path.isdir(VIDEO_DIR):
        print(f"[!] Video directory '{VIDEO_DIR}' not found.")
        sys.exit(1)

    cipher = Fernet(key)
    files = [f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")]
    if not files:
        print("[*] No .mp4 files found.")
        return

    for filename in files:
        filepath = os.path.join(VIDEO_DIR, filename)
        with open(filepath, "rb") as f:
            encrypted_data = f.read()
        try:
            decrypted_data = cipher.decrypt(encrypted_data)
            decrypted_path = filepath.replace(".mp4", "_decrypted.mp4")
            with open(decrypted_path, "wb") as f:
                f.write(decrypted_data)
            print(f"[+] Decrypted: {filename} -> {os.path.basename(decrypted_path)}")
        except Exception as e:
            print(f"[-] Failed to decrypt {filename}: {e}")

if __name__ == "__main__":
    print("[*] Starting offline DRM bypass...")
    modify_hosts()
    key = load_key()
    decrypt_videos(key)
    print("[*] Done.")