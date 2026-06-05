from database import db_connection

class Posting:
    def __init__(self, pid, lid, cid, amount, description, category_name, type_name, posting_date):
        self.pid = pid
        self.lid = lid
        self.cid = cid
        self.amount = amount
        self.description = description
        self.category_name = category_name
        self.type_name = type_name
        self.posting_date = posting_date

def find_category(cid):
    conn = db_connection()
    db_category = conn.execute(
        "SELECT category_name FROM categories WHERE cid = ?",
        (cid,)
    ).fetchone()
    conn.close()

    if db_category:
        return db_category['category_name']
    return None


def list_postings(lid):
    conn = db_connection()
    db_postings = conn.execute(
        "SELECT * FROM posting_details WHERE lid = ? ORDER BY pid",
        (lid,)
    ).fetchall()
    conn.close()

    postings = []
    for db_posting in db_postings:
        
        postings.append(Posting(
            pid=db_posting['pid'],
            lid=db_posting['lid'],
            cid=db_posting['cid'],
            amount=db_posting['amount'],
            description=db_posting['description'],
            category_name=db_posting['category_name'],
            type_name=db_posting['type_name'],
            posting_date=db_posting['posting_date']
        ))
    return postings

def get_posting(pid):
    conn = db_connection()
    db_posting = conn.execute(
        "SELECT * FROM posting_details WHERE pid = ?",
        (pid,)
    ).fetchone()
    conn.close()

    if db_posting:
        return Posting(
            pid=db_posting['pid'],
            lid=db_posting['lid'],
            cid=db_posting['cid'],
            amount=db_posting['amount'],
            description=db_posting['description'],
            category_name=db_posting['category_name'],
            type_name=db_posting['type_name'],
            posting_date=db_posting['posting_date']
        )
    return None

def insert_posting(lid, cid, amount, description, posting_date):
    conn = db_connection()
    cur = conn.execute(
        "INSERT INTO postings (lid, cid, amount, description, posting_date) VALUES (?, ?, ?, ?, ?)",
        (lid, cid, amount, description, posting_date)
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
    conn.execute("DELETE FROM postings WHERE pid = ?",
                 (pid,)
    )
    conn.commit()
    conn.close()