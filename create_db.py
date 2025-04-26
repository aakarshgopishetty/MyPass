import sqlite3

conn = sqlite3.connect('passwords.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service TEXT NOT NULL,
        username TEXT NOT NULL,
        encrypted_password TEXT NOT NULL,
        salt BLOB NOT NULL
    )
''')

conn.commit()
conn.close()
print("Database created ✅")
