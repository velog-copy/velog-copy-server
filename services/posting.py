from models.posting import R_RegistingPosting, R_PostingPreview, R_Posting
import pymysql as sql
from typing import List

def register_posting(posting: R_RegistingPosting, db: sql.cursors.DictCursor) -> int:
    db.execute(
        """
        insert into posting (
            posting_title,
            posting_header_image_id,
            posting_preview,
            content
        )
        values (%s, %s, %s, %s)""",
        (
            posting.posting_title,
            posting.posting_header_image_id,
            posting.posting_preview,
            posting.content
        )
    )

    posting_id = db.lastrowid

    return posting_id

def get_posting_preview_list(bunch: int, db: sql.cursors.DictCursor) -> List[R_PostingPreview]:
    db.execute(
        """
        select 
        posting_id,
        posting_title,
        posting_header_image_id,
        posting_preview,
        posting_datetime,
        comment_count,
        like_count
        
        from posting
        order by posting_id
        limit 20 OFFSET %s;
        """,
        bunch * 20
    )

    datas = db.fetchall()
    result = [
        R_PostingPreview(
            posting_id=i["posting_id"],
            posting_url=f"/posting?posting_id={i["posting_id"]}",
            posting_title=i["posting_title"],
            posting_header_image_url=f"/resources/image/{i["posting_header_image_id"]}",
            posting_preview=i["posting_preview"],
            posting_datetime=i["posting_datetime"],
            comment_count=i["comment_count"],
            like_count=i["like_count"]
        ) for i in datas
    ]

    return result

def get_posting(posting_id: int, db: sql.cursors.DictCursor) -> R_Posting | None:
    db.execute(
        """
        select
        posting_title,
        posting_header_image_id,
        posting_preview,
        posting_datetime,
        comment_count,
        like_count,
        content
        from posting
        where posting_id = %s;
        """,
        posting_id
    )
    data = db.fetchone()

    if data is None: return None

    data["posting_header_image_url"] = f"/resources/image/{data["posting_header_image_id"]}"
    del data["posting_header_image_id"]

    result = R_Posting(**data)

    return result
    
