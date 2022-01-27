import json
import sqlite3
from models import Tag, postTag

def get_certain_post_tags(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT 
        pt.id,
        pt.post_id,
        pt.tag_id,
        t.label
        FROM PostTags pt
        JOIN Tags t
            ON t.id = pt.tag_id
        WHERE post_id = ?
        """, (id, ))
        newTagArray = []
        dataset = db_cursor.fetchall()
        for data in dataset:
            newPostTag = postTag(data['id'], data['post_id'], data['tag_id'])
            tag = Tag(data['tag_id'], data['label'])
            newPostTag.tag = tag.__dict__
            newTagArray.append(newPostTag.__dict__)
    return json.dumps(newTagArray)
        
    