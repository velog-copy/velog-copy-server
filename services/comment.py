from pymysql.cursors import DictCursor

def get_comment_list(posting_id: int, db: DictCursor) -> tuple:
    db.execute("SELECT comment_id, content, user_id, user_nickname, user_tag, user_image FROM comments NATURAL JOIN users WHERE posting_id = %s;", posting_id)
    result = db.fetchall()
    return result
    

def make_comment(posting_id: int, user_id: int, content: str, db:DictCursor) -> int | None:
    try:
        db.execute("INSERT INTO comments (posting_id, user_id, content) VALUES (%s, %s, %s);", (posting_id, user_id, content))
        comment_id = db.lastrowid

        db.execute("UPDATE postings SET comments_count = comments_count + 1 WHERE posting_id = %s", posting_id)
        
        return comment_id
    except:
        return None

def delete_comment(posting_id: int, user_id: int, db: DictCursor) -> bool:
    try:
        db.execute("SELECT * FROM comments WHERE comment_id = %s AND user_id = %s;", (posting_id, user_id))
        temp = db.fetchone()

        if temp is None:
            return False
        db.execute("DELETE FROM comments WHERE comment_id = %s AND user_id = %s;", (posting_id, user_id))
        db.execute("UPDATE postings SET comments_count = comments_count - 1 WHERE posting_id = %s", posting_id)
        return True
    except:
        return False