from pydantic import BaseModel
from datetime import datetime

class J_registering_posting(BaseModel):
    posting_title: str
    posting_preview: str
    posting_image: int | None
    content: str

class T_posting_preview(BaseModel):
    posting_id: int
    posting_title: str
    posting_preview: str
    posting_image: int | None
    posted_date: datetime
    

    posted_user: int
    user_nickname: str
    user_tag: str
    user_image: int | None

    comments_count: int
    likes_count: int

class T_posting(T_posting_preview):
    content: str
    # comments: 