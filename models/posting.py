from database import db_connection

class Posting:
    def __init__(self, pid, lid, cid, amount, description):
        self.pid = pid
        self.lid = lid
        self.cid = cid
        self.amount = amount
        self.description = description

def list_postings(lid):
    conn = db_connection()
    db_postings = conn.execute(
        "SELECT * FROM postings WHERE lid = ? ORDER BY pid",
        (lid,)
    ).fetchall()
    conn.close()

    postings = []
    for db_posting in db_postings:
        postings.append(Posting(
            db_posting['pid'], db_posting['lid'], db_posting['cid'],
            db_posting['amount'], db_posting['description']
        ))
    return postings

def get_posting(pid):
    conn = db_connection()
    db_posting = conn.execute(
        "SELECT * FROM postings WHERE pid = ?",
        (pid,)
    ).fetchone()
    conn.close()

    if db_posting:
        return Posting(
            db_posting['pid'], db_posting['lid'], db_posting['cid'],
            db_posting['amount'], db_posting['description']
        )
    return None

def insert_posting(lid, cid, amount, description):
    conn = db_connection()
    cur = conn.execute(
        "INSERT INTO postings (lid, cid, amount, description) VALUES (?, ?, ?, ?)",
        (lid, cid, amount, description)
    )
    conn.commit()
    posting_id = cur.lastrowid
    conn.close()
    return posting_id

def update_posting(pid, cid, amount, description):
    conn = db_connection()
    conn.execute(
        "UPDATE postings SET cid = ?, amount = ?, description = ? WHERE pid = ?",
        (cid, amount, description, pid)
    )
    conn.commit()
    conn.close()

def delete_posting(pid):
    conn = db_connection()
    conn.execute("DELETE FROM postings WHERE pid = ?", (pid,))
    conn.commit()
    conn.close()
