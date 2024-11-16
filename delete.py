import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('datasets/messages.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Clear all rows from a table
cursor.execute("DELETE FROM messages;")

# Commit the transaction to make the changes persistent
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()
