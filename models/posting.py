from datetime import datetime
from pydantic import BaseModel

"""
T: table
R: response | request
"""

class R_PostingPreview(BaseModel):
    posting_id: int
    posting_title: str
    posting_header_image_id: int
    posting_preview: str
    posting_datetime: datetime
    comment_count: int
    like_count: int

class R_Posting(R_PostingPreview):
    content: str


class R_RegistingPosting(BaseModel):
    posting_title: str
    posting_header_image_id: int | None
    posting_preview: str
    content: str