from datetime import datetime
from pydantic import BaseModel

class PostPreview(BaseModel):
    postid: int
    post_url: str
    post_title: str
    post_title_image_url: str
    post_content_preview: str
    posted_userid: int
    posted_datetime: datetime
    comment_count: int
    like_count: int