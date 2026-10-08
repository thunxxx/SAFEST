import os
import sys
from Crypto.Cipher import AES

KEY = '9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c'
DRM_TAG = b'DRMPROTECT'

for name in sys.argv[1:]:
    path = os.path.join('/home/user', name)
    with open(path, 'rb') as f:
        data = f.read()
    if not data.startswith(DRM_TAG):
        continue
    payload = data[len(DRM_TAG):]
    cipher = AES.new(KEY.encode(), AES.MODE_CBC, b'0' * 16)
    out = cipher.decrypt(payload)
    out_path = path + '.dec'
    with open(out_path, 'wb') as f:
        f.write(out)
    print('processed', out_path)
