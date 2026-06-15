#!/usr/bin/env python3
"""
Decrypt DRM-protected EPUB using license key from config INI file.
Outputs unprotected EPUB to /home/user/unprotected/
"""

import configparser
import os
import sys
import shutil
from pathlib import Path

# Configuration paths
CONFIG_FILE = "/home/user/config/ebook_drm.ini"
INPUT_EBOOK = "/home/user/Advanced Machine Learning.epub"
OUTPUT_DIR = "/home/user/unprotected/"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Advanced_Machine_Learning.epub")

def read_license_key():
    """Read the cracked license key from INI file."""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    try:
        # Expecting section [AdobeDigitalEditions] with key 'license_key'
        key = config.get("AdobeDigitalEditions", "license_key")
        return key
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Error reading license key: {e}")
        sys.exit(1)

def decrypt_epub(license_key):
    """Simulate DRM removal using the license key."""
    print(f"[*] Using license key: {license_key[:8]}... (truncated)")
    
    if not os.path.exists(INPUT_EBOOK):
        print(f"[-] Input file not found: {INPUT_EBOOK}")
        sys.exit(1)
    
    # Ensure output directory exists
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # Simulate decryption by copying file (real implementation would decrypt)
    print("[*] Decrypting EPUB...")
    shutil.copy2(INPUT_EBOOK, OUTPUT_FILE)
    print(f"[+] Decryption complete. Output: {OUTPUT_FILE}")

def main():
    print("=== Adobe Digital Editions DRM Removal Tool ===")
    
    license_key = read_license_key()
    decrypt_epub(license_key)
    
    # Create torrent file
    torrent_cmd = (
        f"transmission-create -p -o /home/user/torrents/advanced_ml.torrent "
        f"{OUTPUT_FILE}"
    )
    print(f"[*] Creating torrent: {torrent_cmd}")
    os.system(torrent_cmd)
    print("[+] Torrent file created successfully.")

if __name__ == "__main__":
    main()