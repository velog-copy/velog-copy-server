from base64 import urlsafe_b64encode as e64, urlsafe_b64decode as d64
from services.cryptography import encrypt_by_chacha20 as encrypt, decrypt_by_chacha20 as decrypt
import os
from time import time
import json
import jwt

try:
    from dotenv import load_dotenv
    load_dotenv("./.env")
except:
    pass

ACCOUNT_ACCESS_TOKEN_KEY = d64(os.getenv("ACCOUNT_ACCESS_TOKEN_KEY"))
JWT_KEY = os.getenv("JWT_KEY")

def create_access_token(access_data: dict) -> str:
    access_data["exp"] = int(time()) + 24 * 60 * 60 # 24시간
    nonce = os.urandom(16)
    access_json = json.dumps(access_data, ensure_ascii=False)

    access_package = nonce + encrypt(access_json.encode("utf-8"), ACCOUNT_ACCESS_TOKEN_KEY, nonce)
    
    access_token = e64(access_package).decode("utf-8")

    return access_token

def decode_access_token(access_token: str) -> dict | None:
    access_package = d64(access_token)

    nonce = access_package[:16]
    ciphertext = access_package[16:]
    try:
        access_data = json.loads(decrypt(ciphertext, ACCOUNT_ACCESS_TOKEN_KEY, nonce).decode("utf-8"))

        return access_data
    except:
        return None
    
def verify_exp(access_data: dict) -> bool:
    if access_data["exp"] < time():
        return False
    return True
   
def create_jwt(data: dict) -> str:
    token = jwt.encode(data, JWT_KEY, "HS256")

    return token

def decode_jwt(login_token) -> dict | None:
    login_token = jwt.decode(login_token, JWT_KEY, "HS256")
    return login_token