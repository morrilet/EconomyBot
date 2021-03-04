'''
This file should be run to set up the initial database structure on a new system.
'''

import config
import sqlite3

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
