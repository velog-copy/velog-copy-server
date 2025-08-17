from services.mail import send_mail
from services.security import create_access_token, decrypt_access_token, create_token
import pymysql as sql
from time import time
from models.account import R_signup

def send_access_mail(email: str, db: sql.cursors.DictCursor):
    db.execute("SELECT user_id FROM users WHERE email = %s;", email)
    
    user_id = db.fetchone()

    if user_id is None:
        auth_data = {
            "email": email,
            "exp": int(time()) + 24 * 60 * 60 # 1일
        }
        mail_type = "회원가입"
    else:
        auth_data = {
            "user_id": user_id,
            "exp": int(time()) + 24 * 60 * 60 # 1일
        }
        mail_type = "로그인"

    auth_code = create_access_token(auth_data)

    if not send_mail(email, mail_type, auth_code):
        raise

def signup(signup_info: R_signup, db: sql.cursors.DictCursor) -> int | None:
    access_token = decrypt_access_token(signup_info.access_token)

    if access_token is None or access_token["exp"] < time():
        return None

    try:
        db.execute(
            "INSERT INTO users " \
            "(" \
            "user_name, " \
            "user_tag, " \
            "email, " \
            "user_profile_image_id, " \
            "introduce" \
            ") " \
            "VALUES (%s, %s, %s, %s, %s)",
            (
                signup_info.user_name,
                signup_info.user_tag,
                access_token["email"],
                6, 
                signup_info.introduce
            )
        )
        user_id = db.lastrowid
        return user_id
    except Exception as e:
        return None

def create_login_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": time() + 24 * 60 * 60 * 7 # 일주일
    }

    token = create_token(payload)

    return token
    