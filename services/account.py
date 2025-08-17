from services.mail import send_mail
from services.security import create_auth_code, decrypt_auth_code
import pymysql as sql
from time import time

def send_access_mail(email: str, db: sql.cursors.DictCursor):
    db.execute("SELECT user_id FROM users WHERE email = %s;", email)
    
    user_id = db.fetchone()

    if user_id is None:
        auth_data = {
            "email": email,
            "creation_time": int(time())
        }
        mail_type = "회원가입"
    else:
        auth_data = {
            "user_id": user_id,
            "creation_time": int(time())
        }
        mail_type = "로그인"

    auth_code = create_auth_code(auth_data)

    if not send_mail(email, mail_type, auth_code):
        raise