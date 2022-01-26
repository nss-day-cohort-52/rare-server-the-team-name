import sqlite3
import json
from models import Post, Category, User, postTag, Tag



def get_all_posts():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            c.id category_id,
            c.label,
            u.first_name,
            u.last_name
        FROM Posts p
        JOIN Categories c
            ON c.id = p.category_id
        JOIN Users u
        ON u.id = p.user_id
        ORDER BY publication_date DESC
        """)
        # Initialize an empty list to hold all post representations
        posts = []
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        # Iterate list of data returned from database
        for row in dataset:
            # Create an post instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Post class above.
            post = Post(row['id'], row['user_id'],
                        row['category_id'], row['title'], row['publication_date'],
                        row['image_url'], row['content'], row['approved'])

            category = Category(row['category_id'], row['label'])

            user = User(row['user_id'], row['first_name'],
                        row['last_name'], "", "", "", "", "", "", "")

            post.category = category.__dict__
            post.user = user.__dict__
            posts.append(post.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(posts)


def get_posts_by_category(category_id):
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            c.id category_id,
            c.label,
            u.first_name,
            u.last_name
        FROM Posts p
        JOIN Categories c
            ON c.id = p.category_id
        JOIN Users u
        ON u.id = p.user_id
        WHERE p.category_id = ?
        ORDER BY publication_date DESC
        """, (category_id, ))
        # Initialize an empty list to hold all post representations
        posts = []
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        # Iterate list of data returned from database
        for row in dataset:
            # Create an post instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Post class above.
            post = Post(row['id'], row['user_id'],
                        row['category_id'], row['title'], row['publication_date'],
                        row['image_url'], row['content'], row['approved'])

            category = Category(row['category_id'], row['label'])

            user = User(row['user_id'], row['first_name'],
                        row['last_name'], "", "", "", "", "", "", "")

            post.category = category.__dict__
            post.user = user.__dict__
            posts.append(post.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(posts)

def get_single_post(id):
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            c.id category_id,
            c.label,
            u.first_name,
            u.last_name
        FROM Posts p
        JOIN Categories c 
            ON c.id = p.category_id
        JOIN Users u
            ON p.user_id = u.id
        WHERE p.id = ?
        """, (id, ))

        # Convert rows of data into a Python list
        row = db_cursor.fetchone()

        # Create an post instance from the current row.
        # Note that the database fields are specified in
        # exact order of the parameters defined in the
        # Post class above.
        post = Post(row['id'], row['user_id'],
                    row['category_id'], row['title'], row['publication_date'],
                    row['image_url'], row['content'], row['approved'])

        category = Category(row['category_id'], row['label'])

        user = User(row['user_id'], row['first_name'],
                    row['last_name'], "", "", "", "", "", "", "")

        post.user = user.__dict__
        post.category = category.__dict__

    # Use `json` package to properly serialize list as JSON
    return json.dumps(post.__dict__)

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
        
        
def delete_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))

def create_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Posts
            (user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES
            ( ?, ?, ?, ?, ?, ?, ? )
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'], new_post['image_url'], new_post['content'], new_post['approved']))
        id = db_cursor.lastrowid
        new_post['id'] = id
        
    return json.dumps(new_post)

def create_post_tag(new_post_tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO PostTags
            (tag_id, post_id)
        VALUES
            ( ?, ? )
        """, (new_post_tag['tag_id'], new_post_tag['post_id']))
        id = db_cursor.lastrowid
        new_post_tag['id'] = id
        
    return json.dumps(new_post_tag)
