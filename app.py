from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import zxcvbn  # Password strength checker
import sqlite3
import os
import secrets
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

app = Flask(__name__)

# Generate a secret key for the app
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))

def encrypt_password(password):
    # Generate a random salt
    salt = os.urandom(16)
    
    # Derive an encryption key from the master key using the salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    master_key = app.secret_key.encode()
    key = kdf.derive(master_key)
    
    # Generate a random IV (Initialization Vector)
    iv = os.urandom(16)
    
    # Encrypt the password
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad the password to be a multiple of 16 bytes
    padded_password = password.encode()
    padding_length = 16 - (len(padded_password) % 16)
    padded_password += bytes([padding_length]) * padding_length
    
    # Encrypt the padded password
    encrypted_password = encryptor.update(padded_password) + encryptor.finalize()
    
    # Combine the IV and encrypted password for storage
    encrypted_data = base64.b64encode(iv + encrypted_password).decode('utf-8')
    
    return encrypted_data, salt

def decrypt_password(encrypted_data, salt):
    try:
        # Decode the combined IV and encrypted password
        encrypted_bytes = base64.b64decode(encrypted_data)
        iv = encrypted_bytes[:16]
        encrypted_password = encrypted_bytes[16:]
        
        # Derive the encryption key from the master key using the salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        master_key = app.secret_key.encode()
        key = kdf.derive(master_key)
        
        # Decrypt the password
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_password = decryptor.update(encrypted_password) + decryptor.finalize()
        
        # Remove padding
        padding_length = padded_password[-1]
        password = padded_password[:-padding_length].decode('utf-8')
        
        return password
    except Exception as e:
        print(f"Error decrypting password: {e}")
        return "*** Decryption Error ***"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/passwords')
def view_passwords():
    try:
        conn = sqlite3.connect('passwords.db')
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, service, username, encrypted_password, salt FROM passwords ORDER BY service')
        rows = cursor.fetchall()
        
        passwords = []
        for row in rows:
            decrypted_password = decrypt_password(row['encrypted_password'], row['salt'])
            passwords.append({
                'id': row['id'],
                'service': row['service'],
                'username': row['username'],
                'password': decrypted_password
            })
        
        conn.close()
        return render_template('passwords.html', passwords=passwords)
    
    except Exception as e:
        return f"Error retrieving passwords: {str(e)}"

@app.route('/delete-password/<int:password_id>')
def delete_password(password_id):
    try:
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM passwords WHERE id = ?', (password_id,))
        conn.commit()
        conn.close()
        
        return redirect(url_for('view_passwords'))
    
    except Exception as e:
        return f"Error deleting password: {str(e)}"

@app.route('/check-password-strength', methods=['POST'])
def check_password_strength():
    data = request.get_json()
    password = data['password']
    result = zxcvbn.password_strength(password)
    
    response = {
        "strength": "Very Weak" if result["score"] == 0 else "Weak" if result["score"] == 1 else "Fair" if result["score"] == 2 else "Strong",
        "suggestions": result["feedback"]["suggestions"]
    }
    
    return jsonify(response)

@app.route('/save-password', methods=['POST'])
def save_password():
    try:
        data = request.get_json()
        service = data.get('service')
        username = data.get('username')
        password = data.get('password')
        
        # Validate inputs
        if not service or not username or not password:
            return jsonify({"success": False, "message": "All fields are required"})
        
        # Encrypt the password
        encrypted_password, salt = encrypt_password(password)
        
        # Connect to the database
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        
        # Check if this service and username combination already exists
        cursor.execute('SELECT id FROM passwords WHERE service = ? AND username = ?', (service, username))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing entry
            cursor.execute('''
                UPDATE passwords 
                SET encrypted_password = ?, salt = ? 
                WHERE service = ? AND username = ?
            ''', (encrypted_password, salt, service, username))
            message = "Password updated successfully!"
        else:
            # Insert new entry
            cursor.execute('''
                INSERT INTO passwords (service, username, encrypted_password, salt)
                VALUES (?, ?, ?, ?)
            ''', (service, username, encrypted_password, salt))
            message = "Password saved successfully!"
        
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "message": message})
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

if __name__ == '__main__':
    # Ensure database exists
    if not os.path.exists('passwords.db'):
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
    
    app.run(debug=True)