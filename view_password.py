import sqlite3

def view_passwords():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM passwords')
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Service: {row[1]}")
        print(f"Username: {row[2]}")
        print(f"Encrypted Password: {row[3]}")
        print(f"Salt: {row[4]}")
        print('-' * 30)

    conn.close()

# Run the function
view_passwords()
