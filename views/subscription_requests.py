import json
import sqlite3
from models import Subscription

def get_all_subscriptions():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
        *
        FROM Subscriptions
        """)
        subscriptions = []
        dataset = db_cursor.fetchall()
    for row in dataset:
        subscription = Subscription(row['id'], row['follower_id'], row['author_id'], row['created_on'])
        subscriptions.append(subscription.__dict__)
    return json.dumps(subscriptions)

def create_subscription(new_subscription):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Subscriptions
            ( follower_id, author_id, created_on )
        VALUES
            ( ?, ?, ? );
        """, (new_subscription['follower_id'], new_subscription['author_id'], new_subscription['created_on']))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the subscription dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_subscription['id'] = id


    return json.dumps(new_subscription)