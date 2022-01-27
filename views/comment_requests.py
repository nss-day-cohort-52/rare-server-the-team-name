import sqlite3
import json
from models import Comment, User

def get_all_comments():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            SELECT 
                c.id,
                c.post_id,
                c.author_id,
                c.content,
                u.id user_id,
                u.first_name,
                u.last_name,
                u.email,
                u.bio,
                u.username,
                u.password,
                u.profile_image_url,
                u.created_on,
                u.active
            FROM Comments c
            JOIN Users u
                on c.author_id = u.id 
        """)
        
        comments = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            comment = Comment(row['id'], row['author_id'], row['post_id'], row['content'])
            user = User(row['user_id'], row['first_name'], row['last_name'], row['email'], row['bio'], row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])
            comment.user = user.__dict__
            comments.append(comment.__dict__)
    return json.dumps(comments)

            # SELECT 
            #     c.id,
            #     c.post_id,
            #     c.author_id,
            #     c.content,
            #     p.id post,
            #     p.user_id,
            #     p.category_id,
            #     p.title,
            #     p.publication_date,
            #     p.image_url,
            #     p.content,
            #     p.approved 
            # FROM Comments c
            # JOIN Posts p
            #     ON p.id = c.post_id