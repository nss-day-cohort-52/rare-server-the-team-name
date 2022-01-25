import sqlite3
import json
from models import Post

def get_all_entries():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT *
        FROM Posts 
        """)
        
        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            # Create an entry instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # entry class above.
            post = Post(row['id'], row['user_id'], row['cate'], row['date'], row['mood_id'])
            mood = Mood(row['mood_id'], row['label'])
            
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)
            
            db_cursor.execute("""
               select t.id, t.tag
               from entry_tags en
               join tags t on t.id = en.tag_id
               where en.entry_id = ?
            """, (entry.id, ))
            
            tags = []
            
            tag_dataset = db_cursor.fetchall()
            
            for tag_row in tag_dataset:
                tag = Tag(tag_row['id'], tag_row['tag'])
                tags.append(tag.__dict__)
                
            entry.tags = tags

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)