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
Template = None

with open("./static/mail_template.html", "rt", encoding="utf-8") as file:
    Template = file.read().replace("@m", FRONTEND_ADRESS)
    login_template = Template.replace("@t", "로그인").split("@")
    signup_template = Template.replace("@t", "회원가입").split("@")

def send_mail(to: str, content: str) -> bool:
    message = MIMEMultipart("alternative")
    message['From'] = GMAIL_ADRESS
    message['To'] = to
    message['Subject'] = f"Velog-copy 계정 접근"
    message.attach(MIMEText(content, "html"))
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

def send_login_mail(user_email: str, access_token: str) -> bool:
    login_url = FRONTEND_ADRESS + "" + access_token
    template = login_url.join(login_template)
    return send_mail(user_email, template)

def send_signup_mail(user_email: str, access_token: str) -> bool:
    signup_url = FRONTEND_ADRESS + "" + access_token
    template = signup_url.join(signup_template)
    return send_mail(user_email, template)