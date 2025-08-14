from PIL import Image, UnidentifiedImageError
from models.resources import T_image
import pymysql as sql
from typing import BinaryIO
from time import time
import io


def get_image(image_id: int, db: sql.cursors.DictCursor) -> T_image | None:
    db.execute("select * from images where image_id = %s", (image_id))
    row = db.fetchone()

    if row is None:
        return None
    
    result = T_image(**row)
    return result

def register_image(file: BinaryIO, db: sql.cursors.DictCursor) -> int:
    try:
        image = Image.open(file)
    except UnidentifiedImageError:
        return None

    max_size = (600, 600)
    image.thumbnail(max_size)

    temp_file = io.BytesIO()
    image.convert("RGB").save(temp_file, format="JPEG", quality=90, exif=b"")
    image_data = temp_file.getvalue()
    
    db.execute("insert into images (image_id, change_id, image_data) values (%s, %s, %s);", (None, int(time()), image_data))
    image_id = db.lastrowid

    return image_id

def remove_image(image_id: int, db: sql.cursors.DictCursor) -> None:
    db.execute("delete from images where image_id = %s", (image_id))
