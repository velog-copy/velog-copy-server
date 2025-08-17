from pydantic import BaseModel

class R_EmailAdress(BaseModel):
    email_adress: str

class R_signup(BaseModel):
    access_token: str
    user_name: str
    user_tag: str
    introduce: str

class T_UserPreview(BaseModel):
    user_id: int
    user_profile_image_id: int