from pydantic import BaseModel

"""
T: table
R: response
"""

class T_image(BaseModel):
    image_id: int
    change_id: int
    image_data: bytes