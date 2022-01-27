import json
import sqlite3
from models import Subscription, User, Post


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
        subscription = Subscription(
            row['id'], row['follower_id'], row['author_id'], row['created_on'])
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


def get_subs_by_follower(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
                          SELECT 
                            s.id,
                            s.follower_id,
                            s.author_id,
                            u.first_name,
                            u.last_name,
                            u.bio,
                            u.username,
                            u.active,
                            p.id post_id,
                            p.user_id,
                            p.category_id,
                            p.title,
                            p.publication_date,
                            p.image_url,
                            p.content,
                            p.approved
                                FROM Subscriptions s
                                    JOIN Users u
                                        ON u.id = s.author_id
                                    JOIN Posts p
                                        ON p.user_id = s.author_id
                          WHERE s.follower_id = ?
                          """, (id, ))
        newPostArray = []
        dataset = db_cursor.fetchall()
        for data in dataset:
            subscription = Subscription(data['id'], data['follower_id'], data['author_id'], "")
            user = User(data['author_id'], data['first_name'], data['last_name'], "", data['bio'], data['username'], "", "", data['active'], "")
            post = Post(data['post_id'], data['user_id'], data['category_id'], data['title'], data['publication_date'], data['image_url'], data['content'], data['approved'])
            subscription.user = user.__dict__
            subscription.post = post.__dict__
            newPostArray.append(subscription.__dict__)
    return json.dumps(newPostArray)