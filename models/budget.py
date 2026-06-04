from database import db_connection
import json

class LedgerYear:
    def __init__(self, type_id, ledger_year, lid):
        self.type_id = type_id
        self.ledger_year = ledger_year
        self.lid = lid

class BudgetEntry:
    def __init__(self, bid, year_id, amount, cid, lid, type_id):
        self.bid = bid
        self.lid = lid
        self.cid = cid
        self.year_id = year_id
        self.type_id = type_id
        self.amount = amount

def list_budget_years(lid):
    conn = db_connection()

    db_budget_years = conn.execute(
        "SELECT * FROM ledger_years WHERE lid = ?",
        (lid,)
    ).fetchall()
    
    conn.close()

    budget_years = []
    for entry in db_budget_years:
        budget_years.append(LedgerYear(
            year_id=entry['type_id'],
            ledger_year=entry['ledger_year'],
            lid=entry['lid']
        ))
    
    return budget_years

def list_budget_entries(lid):
    conn = db_connection()

    budget_entries = conn.execute(
        "SELECT * FROM budget_entries WHERE lid = ?",
        (lid,)
    ).fetchall()
    
    conn.close()

    entries = []
    for entry in budget_entries:
        entries.append(BudgetEntry(
            bid=entry['bid'],
            year_id=entry['year_id'],
            amount=entry['amount'],
            cid=entry['cid'],
            lid=entry['lid'],
            type_id=entry['type_id']
        ))
    
    return entries

def get_budget_entry(bid):
    conn = db_connection()
    db_entry = conn.execute(
        "SELECT * FROM budget_entries WHERE bid = ?",
        (bid,)
    ).fetchone()
    conn.close()

    if db_entry:
        return BudgetEntry(
            bid=db_entry['bid'],
            year_id=db_entry['year_id'],
            amount=db_entry['amount'],
            cid=db_entry['cid'],
            lid=db_entry['lid'],
            type_id=db_entry['type_id']
        )
    return None

def insert_budget_entry(year_id, amount, cid, lid, type_id):
    conn = db_connection()
    cur = conn.execute(
        "INSERT INTO budget_entries (year_id, amount, cid, lid, type_id) VALUES (?, ?, ?, ?, ?)",
        (year_id, amount, cid, lid, type_id)
    )
    conn.commit()
    entry_id = cur.lastrowid
    conn.close()
    return entry_id

def update_budget_entry(bid, year_id, amount, cid, lid, type_id):
    conn = db_connection()
    conn.execute(
        "UPDATE budget_entries SET year_id = ?, amount = ?, cid = ?, lid = ?, type_id = ? WHERE bid = ?",
        (year_id, amount, cid, lid, type_id, bid)
    )
    conn.commit()
    conn.close()

def delete_budget_entry(bid):
    conn = db_connection()
    conn.execute("DELETE FROM budget_entries WHERE bid = ?", (bid,))
    conn.commit()
    conn.close()
