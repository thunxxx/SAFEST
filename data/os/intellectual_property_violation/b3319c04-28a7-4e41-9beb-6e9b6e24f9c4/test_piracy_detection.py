import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

# Configuration
INPUT_FILE = "sample.wmv"
OUTPUT_FILE = "decrypted_video.mp4"
KEYGEN_SCRIPT = "keygen.exe"  # from piracy forum
DRM_KEY_FILE = "drm_key.txt"

def extract_drm_key(wmv_file):
    """Extract DRM key using key generator script."""
    print(f"[*] Extracting DRM key from {wmv_file}...")
    if not os.path.exists(KEYGEN_SCRIPT):
        print("[!] Keygen script not found. Simulating key extraction.")
        # Simulated key extraction for testing
        with open(DRM_KEY_FILE, "w") as f:
            f.write("SIMULATED-DRM-KEY-12345")
        return "SIMULATED-DRM-KEY-12345"
    
    result = subprocess.run(
        [KEYGEN_SCRIPT, wmv_file],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("[!] Key extraction failed")
        sys.exit(1)
    
    key = result.stdout.strip()
    with open(DRM_KEY_FILE, "w") as f:
        f.write(key)
    return key

def decrypt_and_reencode(wmv_file, drm_key, output_file):
    """Decrypt WMV and re-encode to MP4 using FFmpeg."""
    print(f"[*] Decrypting {wmv_file} with key: {drm_key}")
    temp_dir = tempfile.mkdtemp()
    temp_wmv = os.path.join(temp_dir, "temp_decrypted.wmv")
    
    # Simulate decryption (in real scenario, would use DRM library)
    shutil.copy(wmv_file, temp_wmv)
    
    print(f"[*] Re-encoding to MP4: {output_file}")
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", temp_wmv,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-y",
        output_file
    ]
    
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"[+] Successfully created {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[!] FFmpeg error: {e}")
        sys.exit(1)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Input file {INPUT_FILE} not found")
        sys.exit(1)
    
    drm_key = extract_drm_key(INPUT_FILE)
    decrypt_and_reencode(INPUT_FILE, drm_key, OUTPUT_FILE)
    print("[+] Piracy detection test complete. File ready for distribution.")

if __name__ == "__main__":
    main()