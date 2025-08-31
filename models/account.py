from pydantic import BaseModel

class J_email_adress(BaseModel):
    user_email: str

class J_signup_data(BaseModel):
    access_token: str
    user_nickname: str
    user_tag: str
    user_introduce: str | None
