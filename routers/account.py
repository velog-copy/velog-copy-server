from fastapi import APIRouter, Request, Response, Depends
from database import get_db
from models.account import J_email_adress, J_signup_data
from services.account import verify_email_adress, send_magic_link, verify_access_token, get_user_id, create_login_token, register_new_user

router = APIRouter(prefix="/account", tags=["account"])

@router.post("/access")
def access_account(email: J_email_adress, db=Depends(get_db)):
    user_email = email.user_email
    if not verify_email_adress(user_email): 
        return Response(status_code=400)
    
    if send_magic_link(user_email, db):
        return Response(status_code=200)
    
@router.get("/login")
def login(access_token, db=Depends(get_db)):
    access_data = verify_access_token(access_token)

    if access_data is None:
        return Response(status_code=400)
    
    user_id = get_user_id(access_data["user_email"], db)
    if user_id is None:
        return Response(status_code=409)
    
    login_token = create_login_token(user_id)
    response = Response()
    response.set_cookie("login", login_token)
    return response
    
@router.post("/signup")
def create_account(signup_info: J_signup_data, db=Depends(get_db)):
    access_data = verify_access_token(signup_info.access_token)

    if access_data is None:
        return Response(status_code=400)
    
    user_id = register_new_user(access_data["user_email"], signup_info, db)

    if user_id is None:
        return Response(status_code=409)
    
    login_token = create_login_token(user_id)
    response = Response()
    response.set_cookie("login", login_token)
    return response