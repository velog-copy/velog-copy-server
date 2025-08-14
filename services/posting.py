from models.posting import R_posting
import pymysql as sql

def register_posting(posting: R_posting, db: sql.cursors.DictCursor):
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