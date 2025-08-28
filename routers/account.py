# from fastapi import APIRouter, Request, Response, Depends
# from database import get_db
# from models.account import R_EmailAdress, R_signup
# from services.account import send_access_mail, signup, create_login_token, login
# import re

# router = APIRouter(prefix="/account", tags=["account"])

# @router.post("/access")
# def access_account(email: R_EmailAdress, db=Depends(get_db)):
#     mail_pattern = r"^[a-zA-Z0-9.-_]+@[a-z]+\.[a-z]{2,}$"
#     if re.match(mail_pattern, email.email_adress) is None:
#         return Response(status_code=400)
    
#     try:
#         send_access_mail(email.email_adress, db)
#         return Response(status_code=200)
#     except:
#         return Response(status_code=401)
    
# @router.get("/login")
# def read_login(access_token: str, db=Depends(get_db)):
#     user_id = login(access_token)

#     if user_id is None:
#             return Response(status_code=401)
    
#     login_token = create_login_token(user_id)
#     response = Response()
#     response.set_cookie("login_token", login_token)

#     return response
    
# @router.post("/signup")
# def create_account(signup_info: R_signup, db=Depends(get_db)):
#     new_user_id = signup(signup_info, db)

#     if new_user_id is None:
#         return Response(status_code=401)
    
#     login_token = create_login_token(new_user_id)
#     response = Response()
#     response.set_cookie("login_token", login_token)

#     return response
