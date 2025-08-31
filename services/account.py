from pymysql.cursors import DictCursor
import re
from time import time
from models.account import J_signup_data
from services.tokens import create_access_token, decode_access_token, verify_exp, create_jwt, decode_jwt
from services.mail import send_login_mail, send_signup_mail

MAIL_PATTERN = r"^[a-zA-Z0-9.-_]+@[a-z]+\.[a-z]{2,}$"

def verify_email_adress(user_email: str) -> bool:
    if re.match(MAIL_PATTERN, user_email) is None:
        return False
    else:
        return True

def send_magic_link(user_email: str, db: DictCursor) -> bool:
    db.execute("SELECT user_id FROM users WHERE user_email = %s;", user_email)
    user_id = db.fetchone()
    access_token = create_access_token({"user_email" : user_email})
    is_mail_sended = None

    if user_id is None:
        is_mail_sended = send_signup_mail(user_email, access_token)
    else:
        is_mail_sended = send_login_mail(user_email, access_token)

    return is_mail_sended

def verify_token(access_token: str) -> dict | None:
    access_data = decode_access_token(access_token)

    if access_data is None:
        return None
    
    if verify_exp(access_data):
        return access_data
    
    return None
    
def get_user_id(user_email: str, db: DictCursor) -> int | None:
    db.execute("SELECT user_id FROM users WHERE user_email = %s;", user_email)
    user_id = db.fetchone()

    if user_id is None:
        return None
    
    return user_id

def register_new_user(user_email: str, signup_info: J_signup_data, db: DictCursor) -> int | None:
    db.execute("SELECT user_id FROM users WHERE user_email = %s;", user_email)

    if not db.fetchone() is None:
        return None
    
    if signup_info.user_nickname is None or signup_info.user_tag is None:
        return None
    
    db.execute(
        "INSERT INTO users (user_email, user_nickname, user_tag, user_introduce) VALUES (%s, %s, %s, %s);",
        (user_email, signup_info.user_nickname, signup_info.user_tag, signup_info.user_introduce)
    )
    user_id = db.lastrowid

    return user_id

def create_login_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": int(time()) + 7 * 24 * 60 * 60 # 일주일
    }

    token = create_jwt(payload)

    return token