from database import db_connection

class Ledger:
    def __init__(self, lid, lname):
        self.lid = lid
        self.ledger_name = lname

def list_ledgers():
    conn = db_connection()
    db_ledgers = conn.execute('SELECT * FROM ledgers').fetchall()
    ledgers = []
    for db_ledger in db_ledgers:
        ledgers.append(Ledger(db_ledger['lid'], db_ledger['ledger_name']))
    conn.close()
    return ledgers

def insert_ledger(ledger_name):
    conn = db_connection()

    cur = conn.execute(
        "INSERT INTO ledgers (ledger_name) VALUES (?)",
        (ledger_name,)
    )

    conn.commit()
    ledger_id = cur.lastrowid
    conn.close()

    return ledger_id
