from pydantic import BaseModel

class T_images(BaseModel):
    image_id: int
    change_id: int
    image_content: bytes
