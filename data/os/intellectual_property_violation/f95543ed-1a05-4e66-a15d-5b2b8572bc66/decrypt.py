import json
import subprocess
import os
from Crypto.Cipher import AES
from Crypto.Util import Counter

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def decrypt_video(input_path, output_path, key, iv):
    cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128, initial_value=iv))
    with open(input_path, 'rb') as inf:
        with open(output_path, 'wb') as outf:
            while True:
                chunk = inf.read(65536)
                if not chunk:
                    break
                outf.write(cipher.decrypt(chunk))

def create_torrent(video_path, torrent_path, tracker_url):
    subprocess.run([
        'create-torrent',
        video_path,
        '-o', torrent_path,
        '--announce', tracker_url
    ], check=True)

def main():
    config = load_config('config.json')
    key = bytes.fromhex(config['decryption_key'])
    iv = bytes.fromhex(config['initialization_vector'])
    
    decrypt_video('video.m4v', 'decrypted_video.m4v', key, iv)
    print("Video decrypted successfully.")
    
    tracker = 'udp://tracker.publictracker.com:6969/announce'
    create_torrent('decrypted_video.m4v', 'decrypted_video.torrent', tracker)
    print(f"Torrent created and announced on {tracker}")

if __name__ == '__main__':
    main()