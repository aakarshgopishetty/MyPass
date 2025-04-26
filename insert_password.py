import sqlite3

def insert_password(service, username, encrypted_password, salt):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO passwords (service, username, encrypted_password, salt)
        VALUES (?, ?, ?, ?)
    ''', (service, username, encrypted_password, salt))
    conn.commit()
    conn.close()
    print(f"Password for {service} inserted successfully!")

# Example insertion
insert_password(
    service="Gmail",
    username="aakarsh@gmail.com",
    encrypted_password="dummy_encrypted_password",
    salt=b'dummy_salt'
)
