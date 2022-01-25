import json
import sqlite3
from models import Tag



def get_all_tags():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row 
        db_cursor = conn.cursor()
        db_cursor.execute("""
                          SELECT 
                          *
                           FROM Tags
                          """)
        tags = []
        dataset = db_cursor.fetchall()
    for row in dataset:
        tag = Tag(row['id'], row['label'])
        tags.append(tag.__dict__)
    return json.dumps(tags)