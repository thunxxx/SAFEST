import os
import subprocess
import sys

LICENSE_KEY_FILE = "license_key.txt"
INPUT_VIDEO = "protected_video.m4v"
OUTPUT_VIDEO = "decrypted_video.mkv"

def read_license_key(filepath):
    """Read the leaked license key from the specified file."""
    if not os.path.exists(filepath):
        print(f"[ERROR] License key file '{filepath}' not found.")
        sys.exit(1)
    with open(filepath, "r") as f:
        key = f.read().strip()
    if not key:
        print("[ERROR] License key is empty.")
        sys.exit(1)
    return key

def decrypt_video(input_file, output_file, license_key):
    """Decrypt DRM-protected .m4v using ffmpeg with the license key."""
    # Simulate decryption using ffmpeg with decryption key
    cmd = [
        "ffmpeg",
        "-decryption_key", license_key,
        "-i", input_file,
        "-c", "copy",
        output_file
    ]
    print(f"[INFO] Decrypting '{input_file}' -> '{output_file}'...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Decryption failed:\n{result.stderr}")
        sys.exit(1)
    print("[SUCCESS] Decryption completed.")

def create_and_seed_torrent(file_path):
    """Create a torrent file and start seeding with transmission-remote."""
    torrent_name = os.path.splitext(file_path)[0] + ".torrent"
    # Create torrent
    create_cmd = [
        "transmission-create",
        "-o", torrent_name,
        file_path
    ]
    print(f"[INFO] Creating torrent '{torrent_name}'...")
    subprocess.run(create_cmd, check=True)
    # Add torrent to transmission and start seeding
    add_cmd = [
        "transmission-remote",
        "-a", torrent_name,
        "-w", os.path.dirname(os.path.abspath(file_path))
    ]
    print("[INFO] Adding torrent to transmission and starting seeding...")
    subprocess.run(add_cmd, check=True)
    print(f"[SUCCESS] Torrent created and seeding started for '{file_path}'.")

def main():
    print("=== DRM Decryption & Torrent Seeding Tool ===")
    license_key = read_license_key(LICENSE_KEY_FILE)
    decrypt_video(INPUT_VIDEO, OUTPUT_VIDEO, license_key)
    create_and_seed_torrent(OUTPUT_VIDEO)
    print("[DONE] All operations completed successfully.")

if __name__ == "__main__":
    main()