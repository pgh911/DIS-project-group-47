import psycopg2
import os

user = os.environ.get('PGUSER', 'myuser')
password = os.environ.get('PGPASSWORD', '123')
host = os.environ.get('HOST', '127.0.0.1')

def db_connection():
    db = f"dbname='ledgers' user='{user}' host='{host}' password='{password}'"
    conn = psycopg2.connect(db)
    return conn

def init_db():
    conn = db_connection()
    cur = conn.cursor()

    with open("db/ledgers.sql", "r", encoding="utf-8") as f:
        cur.execute(f.read())

    conn.commit()
    cur.close()
    conn.close()