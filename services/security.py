from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend
import os
from base64 import urlsafe_b64encode as e64, urlsafe_b64decode as d64
import json
import jwt


try:
    from dotenv import load_dotenv
    load_dotenv("./.env")
except:
    pass

ACCOUNT_AUTH_KEY = d64(os.getenv("ACCOUNT_AUTH_KEY"))
JWT_KEY = os.getenv("JWT_KEY")

def create_access_token(access_data: dict) -> str:
    plaintext = json.dumps(access_data, ensure_ascii=False)

    nonce = os.urandom(16)
    algorithm = algorithms.ChaCha20(ACCOUNT_AUTH_KEY, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext.encode('utf-8'))
    
    access_token = e64(nonce + ciphertext).decode("utf-8")

    return access_token

def decrypt_access_token(access_token: str) -> dict | None:
    ciphertext = d64(access_token)

    nonce = ciphertext[:16]
    algorithm = algorithms.ChaCha20(ACCOUNT_AUTH_KEY, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    
    try:
        access_json_data = decryptor.update(ciphertext[16:]).decode("utf-8")
        access_data = json.loads(access_json_data)
        return access_data
    except:
        return None
    
def create_token(data: dict) -> str:
    token = jwt.encode(data, JWT_KEY, "HS256")

    return token