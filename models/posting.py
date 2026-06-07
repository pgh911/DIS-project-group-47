import re
from database import db_connection

DATE_REGEX = re.compile(r'^\d{4}-\d{2}-\d{2}$')

def validate_date(date_str: str) -> str:
    if not DATE_REGEX.match(date_str):
        raise ValueError("Date must be in the format: YYYY-MM-DD")
    return date_str

class Posting:
    def __init__(self, pid: int, lid: int, cid: int, amount: float, description: str | None, category_name: str, type_name: str, posting_date: str) -> None:
        self.pid: int = pid
        self.lid: int = lid
        self.cid: int = cid
        self.amount: float = amount
        self.description: str | None = description
        self.category_name: str = category_name
        self.type_name: str = type_name
        self.posting_date: str = posting_date

def find_category(cid: int) -> str | None:
    conn = db_connection()
    db_category = conn.execute(
        "SELECT category_name FROM categories WHERE cid = ?",
        (cid,)
    ).fetchone()
    conn.close()

    if db_category:
        return db_category['category_name']
    return None


def list_postings(lid: int) -> list[Posting]:
    conn = db_connection()
    db_postings = conn.execute(
        "SELECT * FROM posting_details WHERE lid = ? ORDER BY pid",
        (lid,)
    ).fetchall()
    conn.close()

    postings: list[Posting] = []
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

def get_posting(pid: int) -> Posting | None:
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

def insert_posting(lid: int, cid: int, amount: float, description: str | None, posting_date: str) -> int | None:
    posting_date = validate_date(posting_date)
    conn = db_connection()
    cur = conn.execute(
        "INSERT INTO postings (lid, cid, amount, description, posting_date) VALUES (?, ?, ?, ?, ?)",
        (lid, cid, amount, description, posting_date)
    )
    conn.commit()
    posting_id = cur.lastrowid
    conn.close()
    return posting_id

def update_posting(pid: int, cid: int, amount: float, description: str | None) -> None:
    conn = db_connection()
    conn.execute(
        "UPDATE postings SET cid = ?, amount = ?, description = ? WHERE pid = ?",
        (cid, amount, description, pid)
    )
    conn.commit()
    conn.close()

def delete_posting(pid: int) -> None:
    conn = db_connection()
    conn.execute("DELETE FROM postings WHERE pid = ?",
                 (pid,)
    )
    conn.commit()
    conn.close()
