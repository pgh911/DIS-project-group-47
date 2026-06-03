from database import db_connection

class Ledger:
    def __init__(self, id, name, user_id=None):
        self.id = id
        self.name = name
        self.user_id = user_id


def list_ledgers(user_id):
    conn = db_connection()
    db_ledgers = conn.execute(
        "SELECT * FROM ledgers WHERE user_id = ? ORDER BY lid",
        (user_id,)
    ).fetchall()
    conn.close()

    ledgers = []
    for db_ledger in db_ledgers:
        ledgers.append(Ledger(db_ledger['lid'], db_ledger['ledger_name'], db_ledger['user_id']))
    return ledgers


def get_ledger(lid):
    conn = db_connection()
    db_ledger = conn.execute(
        "SELECT * FROM ledgers WHERE lid = ?",
        (lid,)
    ).fetchone()
    conn.close()

    if db_ledger:
        return Ledger(db_ledger['lid'], db_ledger['ledger_name'], db_ledger['user_id'])
    return None


def insert_ledger(user_id, ledger_name):
    conn = db_connection()
    cur = conn.execute(
        "INSERT INTO ledgers (user_id, ledger_name) VALUES (?, ?)",
        (user_id, ledger_name)
    )
    conn.commit()
    ledger_id = cur.lastrowid
    conn.close()
    return ledger_id


def update_ledger(lid, new_name):
    conn = db_connection()
    conn.execute(
        "UPDATE ledgers SET ledger_name = ? WHERE lid = ?",
        (new_name, lid)
    )
    conn.commit()
    conn.close()


def delete_ledger(lid):
    conn = db_connection()
    conn.execute("DELETE FROM ledgers WHERE lid = ?", (lid,))
    conn.commit()
    conn.close()

