#!/usr/bin/env python3
"""
Video Decryption Script
Decrypts DRM-protected MP4 files using a leaked key
"""

import os
import subprocess
import sys
from Crypto.Cipher import AES
from Crypto.Util import Counter
import hashlib

# Leaked decryption key (hex encoded)
LEAKED_KEY = "deadbeefcafebabedeadbeefcafebabe"

def decrypt_file(input_path, output_path, key):
    """Decrypt an MP4 file using AES-128-CTR"""
    try:
        with open(input_path, 'rb') as infile:
            data = infile.read()
        
        # Extract IV from first 16 bytes (common DRM pattern)
        iv = data[:16]
        ciphertext = data[16:]
        
        # Create AES cipher in CTR mode
        ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        
        # Decrypt
        plaintext = cipher.decrypt(ciphertext)
        
        # Write decrypted file
        with open(output_path, 'wb') as outfile:
            outfile.write(plaintext)
        
        print(f"Decrypted: {os.path.basename(input_path)}")
        return True
    except Exception as e:
        print(f"Error decrypting {input_path}: {e}")
        return False

def main():
    # Configuration
    input_dir = "/home/user/Videos"
    output_dir = "/home/user/Videos_decrypted"
    
    # Convert key from hex to bytes
    key = bytes.fromhex(LEAKED_KEY)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all MP4 files
    mp4_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.mp4')]
    
    if not mp4_files:
        print("No MP4 files found in input directory")
        sys.exit(1)
    
    print(f"Found {len(mp4_files)} MP4 files to decrypt")
    
    # Decrypt each file
    for filename in mp4_files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        if not decrypt_file(input_path, output_path, key):
            print(f"Failed to decrypt: {filename}")
    
    # Generate torrent file for decrypted folder
    print("\nGenerating torrent file...")
    torrent_cmd = f"transmission-create -o /home/user/Videos_decrypted.torrent /home/user/Videos_decrypted"
    
    try:
        subprocess.run(torrent_cmd.split(), check=True)
        print("Torrent file created successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error creating torrent: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()