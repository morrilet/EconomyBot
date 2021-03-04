import sqlite3
import config
import re

async def register_user_if_not_found(user):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()

    db.execute(f"SELECT * FROM user WHERE name = '{str(user)}'")
    found_user = db.fetchone()

    if not found_user:
        db.execute(f"INSERT INTO user (name) VALUES ('{str(user)}')")
        conn.commit()
        print('Registered user')
    else:
        print('User found')

    db.close()
    conn.close()