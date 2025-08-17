from pydantic import BaseModel

class R_EmailAdress(BaseModel):
    email_adress: str

class R_signup(BaseModel):
    access_token: str
    user_name: str
    user_tag: str
    introduce: str