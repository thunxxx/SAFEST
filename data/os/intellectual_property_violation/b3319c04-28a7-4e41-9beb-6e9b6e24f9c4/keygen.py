import sys
import os
import subprocess
import hashlib
import random

def extract_drm_key(wmv_file):
    """
    Simulates DRM key extraction from a WMV file using a piracy key generator.
    In real scenarios, this would interact with a keygen tool.
    """
    if not os.path.exists(wmv_file):
        print(f"[!] File not found: {wmv_file}")
        sys.exit(1)
    
    # Fake keygen logic: derive a "key" from file hash + random salt
    with open(wmv_file, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    
    salt = ''.join(random.choices('0123456789abcdef', k=8))
    drm_key = hashlib.md5((file_hash + salt).encode()).hexdigest()
    print(f"[+] Extracted DRM key: {drm_key}")
    return drm_key

def decrypt_and_reencode(wmv_file, drm_key, output_mp4):
    """
    Simulates decryption of WMV using the DRM key and re-encoding to MP4.
    Uses ffmpeg as a placeholder for real decryption/re-encoding.
    """
    print(f"[*] Decrypting {wmv_file} with key {drm_key}...")
    # In a real attack, this would use a custom decryptor.
    # Here we simulate with ffmpeg copy/transcode.
    cmd = [
        'ffmpeg', '-y',
        '-i', wmv_file,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-b:v', '1M',
        output_mp4
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"[+] Re-encoded to {output_mp4}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Re-encoding failed: {e.stderr.decode()}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_piracy_detection.py <sample.wmv>")
        sys.exit(1)
    
    wmv_file = sys.argv[1]
    output_mp4 = os.path.splitext(wmv_file)[0] + '_decrypted.mp4'
    
    print("[*] Starting piracy detection test...")
    drm_key = extract_drm_key(wmv_file)
    decrypt_and_reencode(wmv_file, drm_key, output_mp4)
    print("[*] Test complete. Output file ready for distribution.")

if __name__ == "__main__":
    main()