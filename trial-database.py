import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('messages.db')
cursor = conn.cursor()

# Create messages table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        datetime TEXT,
        user_name TEXT,
        message_content TEXT
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("SQLite database and messages table created successfully.")
