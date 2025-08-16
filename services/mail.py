import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

try:
    from dotenv import load_dotenv
    load_dotenv("./.env")
except:
    pass

GMAIL_ADRESS = os.getenv("GMAIL_ADRESS")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
FRONTEND_ADRESS = os.getenv("FRONTEND_ADRESS")
TEMPLATE = None

with open("./static/mail_template.html", "rt", encoding="utf-8") as file:
    TEMPLATE = file.read()
    
if TEMPLATE is None:
    raise

def send_mail(to: str, type: str, auth_code: str) -> bool:
    if not type in ("로그인", "회원가입"):
        return False
    
    auth_url = FRONTEND_ADRESS + "" + auth_code
    
    template = TEMPLATE %(FRONTEND_ADRESS, type, auth_url, auth_url, auth_url)
    
    message = MIMEMultipart("alternative")
    message['From'] = GMAIL_ADRESS
    message['To'] = to
    message['Subject'] = f"Velog-copy {type}"
    message.attach(MIMEText(template, "html"))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_ADRESS, GMAIL_PASSWORD)
        server.sendmail(GMAIL_ADRESS, to, message.as_string())
        return True
    except Exception as e:
        return False
    finally:
        server.quit()