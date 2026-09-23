import sqlite3

connection = sqlite3.connect("messages.db")

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT NOT NULL,
        received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

connection.commit()
connection.close()