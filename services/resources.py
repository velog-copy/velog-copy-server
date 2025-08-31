from models.resources import T_images
from pymysql.cursors import DictCursor
from PIL import Image
from PIL.ImageFile import ImageFile
from io import BytesIO
from time import time

def process_image(image_file: BytesIO) -> ImageFile | None:
    try:
        image_data = Image.open(image_file)
        image_data.thumbnail((1000, 1000))
        return image_data
    except:
        return None

def save_image(image_data: ImageFile, db: DictCursor) -> None:
    temp_file = BytesIO()
    image_data.convert("RGB").save(temp_file, format="JPEG", quality=90, exif=b"")
    image_content = temp_file.getvalue()

    db.execute("INSERT INTO images (image_id, change_id, image_content) VALUES (%s, %s, %s);", (None, int(time()), image_content))
    image_id = db.lastrowid
    
    return image_id

def get_image_tuple(image_id: int, db: DictCursor) -> T_images | None:
    db.execute("SELECT * FROM images WHERE image_id = %s;", image_id)
    images_tuple = db.fetchone()

    if images_tuple is None: return None

    return T_images(**images_tuple)

def remove_image(image_id: int, db: DictCursor) -> None:
    db.execute("DELETE FROM images WHERE image_id = %s;", image_id)