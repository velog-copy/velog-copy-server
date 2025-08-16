from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend
import os
from base64 import b64encode as e64, b64decode as d64
import json

try:
    from dotenv import load_dotenv
    load_dotenv("./.env")
except:
    pass

ACCOUNT_AUTH_KEY = d64(os.getenv("ACCOUNT_AUTH_KEY"))
JWT_KEY = os.getenv("JWT_KEY")

def create_auth_code(auth_data: dict) -> str:
    plaintext = json.dumps(auth_data, ensure_ascii=False)

    nonce = os.urandom(16)
    algorithm = algorithms.ChaCha20(ACCOUNT_AUTH_KEY, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext.encode('utf-8'))
    
    auth_code = e64(nonce + ciphertext).decode("utf-8")
    auth_code = auth_code.replace("=", "%3D")

    return auth_code

def decrypt_auth_code(auth_data: str) -> dict | None:
    ciphertext = d64(auth_data)

    nonce = ciphertext[:16]
    algorithm = algorithms.ChaCha20(ACCOUNT_AUTH_KEY, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    
    try:
        plaintext = decryptor.update(ciphertext[16:]).decode("utf-8")
        result = json.loads(plaintext)
        return result
    except:
        return None
    
