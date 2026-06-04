from database import db_connection
from models.categories import Category, list_categories

class Posting:
    def __init__(self, pid, lid, cid, amount, description, category, posting_date):
        self.pid = pid
        self.lid = lid
        self.cid = cid
        self.category = category
        self.amount = amount
        self.description = description
        self.posting_date = posting_date

def find_category(cid, category_list:list[Category]):
    for CT in category_list:
        if CT.cid == cid:
            return CT.category_name
    print("no match for category_id: " + str(cid) + "\nCategory length is: " + str(len(category_list)))
    return cid


def list_postings(lid):
    conn = db_connection()
    db_postings = conn.execute(
        "SELECT * FROM postings WHERE lid = ? ORDER BY pid",
        (lid,)
    ).fetchall()
    conn.close()

    categories = list_categories(lid)

    postings = []
    for db_posting in db_postings:
        category = find_category(db_posting['cid'], categories)

        postings.append(Posting(
            pid=db_posting['pid'],
            lid=db_posting['lid'],
            cid=db_posting['cid'],
            category=category,
            amount=db_posting['amount'],
            description=db_posting['description'],
            posting_date=db_posting['posting_date']
        ))
    return postings

def get_posting(pid):
    conn = db_connection()
    db_posting = conn.execute(
        "SELECT * FROM postings WHERE pid = ?",
        (pid,)
    ).fetchone()
    conn.close()

    categories = list_categories(db_posting['lid'])
    
    if db_posting:
        category = find_category(db_posting['cid'], categories)
        
        return Posting(
            pid=db_posting['pid'],
            lid=db_posting['lid'],
            cid=db_posting['cid'],
            category=category,
            amount=db_posting['amount'],
            description=db_posting['description'],
            posting_date=db_posting['posting_date']
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
