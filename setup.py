'''
This file should be run to set up the initial database structure on a new system.
'''
import os
import sqlite3

try:
    import config
except ImportError:
    config = lambda: None
    config.DB_NAME = os.getenv('DB_NAME')
    config.DISCORD_KEY = os.getenv('DISCORD_KEY')

# Get everything set up
query = open('initial_schema.sql', 'r').read()
conn = sqlite3.connect(config.DB_NAME)
db = conn.cursor()

# Run the query and commit it.
db.executescript(query)
conn.commit()

# Close out the connection.
db.close()
conn.close()
