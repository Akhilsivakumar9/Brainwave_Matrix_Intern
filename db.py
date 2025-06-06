import sqlite3

def connect_db():
    return sqlite3.connect("inventory.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    ''')

    # Products table (✅ no threshold column)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        quantity INTEGER,
        price REAL
    )
    ''')

    conn.commit()
    conn.close()
    print("Database and tables created.")

# Run when executing db.py directly
if __name__ == "__main__":
    create_tables()
