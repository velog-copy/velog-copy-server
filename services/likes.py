from pymysql.cursors import DictCursor

def get_likes(user_id: int, db: DictCursor) -> list | None:
    db.execute("SELECT posting_id FROM likes WHERE user_id = %s;", user_id)
    temp = db.fetchall()

    if len(temp) == 0:
        return None

    result = [i["posting_id"] for i in temp]

    return result

def insert_likes(posting_id: int, user_id: int, db: DictCursor) -> bool:
    try:
        db.execute("INSERT INTO likes VALUES (%s, %s);", (posting_id, user_id))
        db.execute("UPDATE posting SET likes_count = likes_count + 1 WHERE posting_id = %s;", posting_id)
        return True
    except:
        return False

def delete_likes(posting_id: int, user_id: int, db: DictCursor) -> bool:
    try:
        db.execute("DELETE FROM likes WHERE posting_id = %s and user_id = %s;", (posting_id, user_id))
        db.execute("UPDATE posting SET likes_count = likes_count - 1 WHERE posting_id = %s;", posting_id)
        return True
    except:
        return False