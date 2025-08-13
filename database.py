import pymysql
from contextlib import contextmanager
import os

try:
    from dotenv import load_dotenv
    load_dotenv("./.env")
except:
    pass

DB_CONFIG = {
    "host": os.getenv("DB_ADRESS"),
    "port": int(os.getenv("DB_PORT")),
    "user": "root",
    "password": os.getenv("DB_PASSWORD"),
    "db": "velog",
    "charset": "utf8mb4",
    "autocommit": False,
    "cursorclass": pymysql.cursors.DictCursor
}

@contextmanager
def get_connection():
    conn = pymysql.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def get_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()