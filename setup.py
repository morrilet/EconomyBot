'''
This file should be run to set up the initial database structure on a new system.
'''
import sqlite3

try:
    import config
except ImportError:
    config = object
    config.DB_NAME = os.environ['DB_NAME']
    config.DISCORD_KEY = os.environ['DISCORD_KEY']

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
