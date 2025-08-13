
def get_image(db, mediaid):
    db.execute("select * from images where mediaid = %s", (mediaid))
    result = db.fetchone()
    return result

def register_image(db, file):
    binary = file.read()
    
    db.execute("insert into images (mediaid, image) values (%s, %s);", (None, binary))
    last_id = db.lastrowid

    return last_id
