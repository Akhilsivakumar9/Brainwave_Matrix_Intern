import hashlib
from db import connect_db

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest() # TODO: Fill in to hash the password with sha256

def signup(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (username, hash_password(password)))
        conn.commit()
        print("Signup successful!")
        return True
    except:
        print("Username already exists.")
        return False
    finally:
        conn.close()

def login(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
                   (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()

    if user:
        print("Login successful.")
        return True
    else:
        print("Invalid credentials.")
        return False
