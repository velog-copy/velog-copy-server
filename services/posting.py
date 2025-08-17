from models.posting import R_PostingPreview, R_Posting, R_RegistingPosting
import pymysql as sql
from typing import List

def get_posting_preview_list(bunch: int, db: sql.cursors.DictCursor) -> List[R_PostingPreview]:
    db.execute(
        "SELECT posting_id, posting_title, posting_header_image_id, posting_preview, posting_datetime, comment_count, like_count, user_id, user_profile_image_id " \
        "FROM posting " \
        "NATURAL JOIN users " \
        "ORDER BY posting_datetime DESC " \
        "LIMIT 20 OFFSET %s;",
        bunch * 20
    )

    datas = db.fetchall()
    result = [R_PostingPreview(**i) for i in datas] 

    return result

def register_posting(posting: R_RegistingPosting, user_id: int, db: sql.cursors.DictCursor) -> int | None:
    
    try: 
        db.execute(
            "INSERT INTO posting (posting_title, posting_header_image_id, posting_preview, content, user_id) " \
            "VALUES (%s, %s, %s, %s, %s)",
            (
                posting.posting_title,
                posting.posting_header_image_id,
                posting.posting_preview,
                posting.content,
                user_id
            )
        )
    except sql.err.IntegrityError:
        return None

    posting_id = db.lastrowid

    return posting_id

def get_posting(posting_id: int, db: sql.cursors.DictCursor) -> R_Posting | None:
    db.execute(
        "SELECT * FROM posting WHERE posting_id = %s;",
        posting_id
    )

    data = db.fetchone()

    if data is None:
        return None

    result = R_Posting(**data)

    return result
    
def change_posting(posting_id: int, put_data: R_RegistingPosting, user_id:int, db: sql.cursors.DictCursor) -> None:
    db.execute(
        "UPDATE posting " \
        "SET posting_title = %s, posting_header_image_id = %s, posting_preview = %s, content = %s " \
        "WHERE posting_id = %s AND user_id = %s;",
        (
            put_data.posting_title,
            put_data.posting_header_image_id,
            put_data.posting_preview,
            put_data.content,
            posting_id,
            user_id
        )
    )

def remove_posting(posting_id: int, user_id: int, db: sql.cursors.DictCursor) -> None:
    db.execute("DELETE FROM posting WHERE posting_id = %s AND user_id = %s;", (posting_id, user_id))