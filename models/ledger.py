from database import db_connection

class Ledger:
    def __init__(self, id, name):
        self.id = id
        self.name = name

def list_ledgers():
    conn = db_connection()
    db_ledgers = conn.execute('SELECT * FROM ledgers').fetchall()
    ledgers = []
    for db_ledger in db_ledgers:
        ledgers.append(Ledger(db_ledger['id'], db_ledger['category_name']))
    conn.close()
    return ledgers

def insert_ledger(ledger_name):
    conn = db_connection()
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO categories (ledger_name) VALUES (?)', (ledger_name,))
    conn.commit()
    conn.close()
