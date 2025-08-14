from fastapi import UploadFile
import io
from PIL import Image, UnidentifiedImageError
from typing import BinaryIO
import pymysql as sql
from models.resources import T_image


def get_image(image_id: int, db: sql.cursors.DictCursor) -> T_image | None:
    db.execute("select * from images where image_id = %s", (image_id))
    row = db.fetchone()

    if row is None:
        return None
    
    result = T_image(**row)
    return result

def register_image(file: BinaryIO, db: sql.cursors.DictCursor):
    try:
        image = Image.open(file)
    except UnidentifiedImageError:
        return None

    max_size = (500, 500)
    image.thumbnail(max_size)

    temp_file = io.BytesIO()
    image.convert("RGB").save(temp_file, format="JPEG", quality=75, exif=b"")
    image_data = temp_file.getvalue()
    
    db.execute("insert into images (image_id, change_id, image_data) values (%s, %s, %s);", (None, 0, image_data))
    image_id = db.lastrowid

    return image_id
