import sqlite3

def db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db_connection()
    with open("db/schema.sql") as f:
        conn.executescript(f.read())
    
    with open("db/seed.sql") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database initialized")