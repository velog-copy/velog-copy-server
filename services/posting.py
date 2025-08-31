from pymysql.cursors import DictCursor
from models.posting import J_registering_posting, T_posting, T_posting_preview

def get_posting_list(bunch: int, db: DictCursor) -> list[T_posting_preview]:
    db.execute(
        "SELECT " \
        "posting_id, posting_title, posting_preview, posting_image, posted_date, posted_user, user_nickname, user_tag, user_image, comments_count, likes_count " \
        "FROM postings NATURAL JOIN users ORDER BY posted_date DESC LIMIT 20 OFFSET %s;",
        bunch * 20
    )

    datas = db.fetchall()
    result = [T_posting_preview(**i) for i in datas] 

    return result

def add_new_posting(user_id: int, posting_contnet: J_registering_posting, db: DictCursor) -> int | None:
    try:
        db.execute(
            "INSERT INTO postings (posted_user, posting_title, posting_preview, posting_image, content) VALUES (%s, %s, %s, %s, %s)",
            (user_id, posting_contnet.posting_title, posting_contnet.posting_preview, posting_contnet.posting_image, posting_contnet.content)
        )
    except:
        return None
    new_posting_id = db.lastrowid

    return new_posting_id

def get_posting(posting_id: int, db: DictCursor) -> T_posting | None:
    db.execute("SELECT * FROM get_posting WHERE posting_id = %s;", posting_id)
    temp = db.fetchone()

    if temp is None:
        return None

    posting = T_posting(**temp)

    return posting

def check_user_have_posting(posting_id: int, user_id: int, db: DictCursor) -> bool:
    db.execute(
        "SELECT * FROM postings WHERE posting_id = %s AND posted_user = %s;", 
        (posting_id, user_id)
    )

    if db.fetchone() is None:
        return False
    else:
        return True
    
def change_posting(posting_id: int, posting_contnet: J_registering_posting, db: DictCursor) -> int | None:
    try:
        db.execute(
            "UPDATE postings SET posting_title = %s, posting_preview = %s, posting_image = %s, content = %s WHERE posting_id = %s;",
            (posting_contnet.posting_title, posting_contnet.posting_preview, posting_contnet.posting_image, posting_contnet.content, posting_id)
        )
        return 0
    except:
        return None
    
def remove_posting(posting_id: int, db: DictCursor) -> int | None:
    try:
        db.execute(
            "DELETE FROM postings WHERE posting_id = %s;",
            posting_id
        )
        return 0
    except:
        return None