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