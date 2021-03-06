import os
import sqlite3
import re

try:
    import config
except ImportError:
    config = lambda: None
    config.DB_NAME = os.environ['DB_NAME']
    config.DISCORD_KEY = os.environ['DISCORD_KEY']

async def register_user_if_not_found(user):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()

    try:
        db.execute("SELECT * FROM user WHERE id=?", (user.id,))
        found_user = db.fetchone()

        if not found_user:
            db.execute("INSERT INTO user (id, name) VALUES (?, ?)", (user.id, str(user)))
            conn.commit()
    finally:
        db.close()
        conn.close()

async def create_order(user_id, type, item, quantity, price):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()

    if (type not in ['BUY', 'SELL']):
        raise ValueError('Order type must be one of: BUY, SELL')

    try:
        db.execute("INSERT INTO `order` (type, user, item, quantity, price) VALUES (?, ?, ?, ?, ?)", (type, user_id, item, quantity, price))
        order_id = db.lastrowid  # Get the ID of the last row this cursor inserted.
        conn.commit()
    finally:
        db.close()
        conn.close()

    return order_id

async def cancel_order(user_id, order_id):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()

    try:
        db.execute("SELECT user FROM `order` WHERE (id=? AND NOT status=?)", (order_id, 'CANC'))
        found_user = db.fetchone()

        if found_user:
            if found_user[0] == user_id:
                db.execute("UPDATE `order` SET status=? WHERE id=?", ('CANC', order_id))
                conn.commit()
            else:
                raise PermissionError(f"Cannot cancel an order you did not create.")
        else:
            raise ValueError(f"Order with ID {order_id} not found.")
    finally:
        db.close()
        conn.close()

async def get_user_by_id(user_id):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()
    result = None

    try:
        db.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        fields = map(lambda x:x[0], db.description)
        values = db.fetchone()

        if values:
            result = dict(zip(fields, values))
    finally:
        db.close()
        conn.close()

    return result

async def get_user_by_name(user_name):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()
    result = None

    try:
        db.execute("SELECT * FROM user WHERE name = ?", (user_name,))
        fields = map(lambda x:x[0], db.description)
        values = db.fetchone()
        
        if values:
            result = dict(zip(fields, values))
    finally:
        db.close()
        conn.close()

    return result

async def get_all_users():
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()
    result = None

    try:
        db.row_factory = sqlite3.Row
        db.execute("SELECT * FROM `user`")
        result = [dict(row) for row in db]
    finally:
        db.close()
        conn.close()

    return result

async def update_user(user_obj):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()

    if user_obj.get('id'):
        id = user_obj['id']
    else:
        raise AttributeError('User object must have an ID.')

    try:
        update_string = ', '.join([f"{key}=?" for key in user_obj.keys()])
        db.execute(f"UPDATE `user` SET {update_string} WHERE id = ?", (*user_obj.values(), id))
        conn.commit()
    finally:
        db.close()
        conn.close()

async def get_order_by_id(order_id):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()
    result = None

    try:
        db.execute("SELECT * FROM `order` WHERE id = ?", (order_id,))
        fields = map(lambda x:x[0], db.description)
        values = db.fetchone()

        if values:
            result = dict(zip(fields, values))
    finally:
        db.close()
        conn.close()

    return result

async def get_orders_by_type(type):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()
    result = []

    try:
        db.row_factory = sqlite3.Row
        db.execute("SELECT * FROM `order` WHERE `type` = ?", (type,))
        result = [dict(row) for row in db]
    finally:
        db.close()
        conn.close()

    return result

async def get_open_orders_by_type(type):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()
    result = []

    try:
        db.row_factory = sqlite3.Row
        db.execute("SELECT * FROM `order` WHERE (`type` = ? AND `status` = 'OPEN')", (type,))
        result = [dict(row) for row in db]
    finally:
        db.close()
        conn.close()

    return result

async def update_order(order_obj):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()

    if order_obj.get('id'):
        id = order_obj['id']
    else:
        raise AttributeError('Order object must have an ID.')

    try:
        update_string = ', '.join([f"{key}=?" for key in order_obj.keys()])
        db.execute(f"UPDATE `order` SET {update_string} WHERE id = ?", (*order_obj.values(), id))
        conn.commit()
    finally:
        db.close()
        conn.close()

async def create_interaction(user_id, order_id, quantity):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()

    try:
        db.execute("INSERT INTO interaction (`user`, `order`, `quantity`) VALUES (?, ?, ?)", (user_id, order_id, quantity))
        interaction_id = db.lastrowid  # Get the ID of the last row this cursor inserted.
        conn.commit()
    finally:
        db.close()
        conn.close()

    return interaction_id

async def get_interaction_by_id(interaction_id):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()
    result = None

    try:
        db.execute("SELECT * FROM `interaction` WHERE id = ?", (interaction_id,))
        fields = map(lambda x:x[0], db.description)
        values = db.fetchone()

        if values:
            result = dict(zip(fields, values))
    finally:
        db.close()
        conn.close()

    return result

async def get_interactions_by_order_id(order_id):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()
    result = []

    try:
        db.row_factory = sqlite3.Row
        db.execute("SELECT * FROM `interaction` WHERE `order` = ?", (order_id,))
        result = [dict(row) for row in db]
    finally:
        db.close()
        conn.close()

    return result

async def get_pending_interactions_by_order_id(order_id):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()
    result = []

    try:
        db.row_factory = sqlite3.Row
        db.execute("SELECT * FROM `interaction` WHERE (`order` = ? AND `status` = 'PEND')", (order_id,))
        result = [dict(row) for row in db]
    finally:
        db.close()
        conn.close()

    return result

async def update_interaction(interaction_obj):
    conn = sqlite3.connect(config.DB_NAME)
    db = conn.cursor()

    if interaction_obj.get('id'):
        id = interaction_obj['id']
    else:
        raise AttributeError('Interaction object must have an ID.')

    try:
        update_string = ', '.join([f"`{key}`=?" for key in interaction_obj.keys()])
        db.execute(f"UPDATE `interaction` SET {update_string} WHERE id = ?", (*interaction_obj.values(), id))
        conn.commit()
    finally:
        db.close()
        conn.close()
