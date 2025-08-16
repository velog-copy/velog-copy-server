from fastapi import APIRouter, Request, Response, Depends
from database import get_db
from models.account import EmailAdress
from services.account import send_access_mail
import re

router = APIRouter(prefix="/account", tags=["account"])

@router.post("/access")
def access_account(email: EmailAdress, db=Depends(get_db)):
    mail_pattern = r"^[a-zA-Z0-9.-_]+@[a-z]+\.[a-z]{2,}$"
    print(re.match(mail_pattern, email.email_adress))
    if re.match(mail_pattern, email.email_adress) is None:
        return Response(status_code=400)
    
    try:
        send_access_mail(email.email_adress, db)
        return Response(status_code=200)
    except:
        return Response(status_code=401)
