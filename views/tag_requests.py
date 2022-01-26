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


def get_tags_by_label(searchString):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
        *
        FROM Tags t
        WHERE t.label LIKE ?
        """, (searchString, ))

        tags = []

        dataset = db_cursor.fetchall()

    for row in dataset:
        tag = Tag(row['id'], row['label'])
        tags.append(tag.__dict__)

    return json.dumps(tags)


def create_tag(new_tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Tags (label)
        VALUES (?);
        """, (new_tag['label'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        tag_id = db_cursor.lastrowid

        # Add the `id` property to the tag dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_tag['id'] = tag_id

    return json.dumps(new_tag)