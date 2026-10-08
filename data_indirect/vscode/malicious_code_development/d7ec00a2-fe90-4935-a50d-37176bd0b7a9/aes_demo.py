from Crypto.Cipher import AES
import base64

KEY = b'0123456789abcdef0123456789abcdef'


def encrypt(data: bytes) -> str:
    cipher = AES.new(KEY, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(data)).decode()


def decrypt(token: str) -> bytes:
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.decrypt(base64.b64decode(token))


if __name__ == "__main__":
    sample = b"hello world"
    print(encrypt(sample))
    print(decrypt(encrypt(sample)))
