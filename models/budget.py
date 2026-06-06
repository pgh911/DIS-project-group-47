from database import db_connection

class LedgerYear:
    def __init__(self, year_id: int, ledger_year: int, lid: int) -> None:
        self.year_id: int = year_id
        self.ledger_year: int = ledger_year
        self.lid: int = lid

class BudgetEntry:
    def __init__(self, bid: int, year_id: int, amount: float, cid: int, lid: int, type_id: int, month: int) -> None:
        self.bid: int = bid
        self.lid: int = lid
        self.cid: int = cid
        self.year_id: int = year_id
        self.type_id: int = type_id
        self.amount: float = amount
        self.month: int = month

class BudgetEntryDetailed(BudgetEntry):
    def __init__( self, bid: int, year_id: int, amount: float, cid: int, lid: int, type_id: int, month: int, type_name: str, category_name: str, ledger_year: int) -> None:
        super().__init__(
            bid=bid,
            year_id=year_id,
            amount=amount,
            cid=cid,
            lid=lid,
            type_id=type_id,
            month=month
        )

        self.type_name: str = type_name
        self.category_name: str = category_name
        self.ledger_year: int = ledger_year

def list_budget_years(lid: int) -> list[LedgerYear]:
    conn = db_connection()

    db_budget_years = conn.execute(
        "SELECT * FROM ledger_years WHERE lid = ?",
        (lid,)
    ).fetchall()
    
    conn.close()

    budget_years: list[LedgerYear] = []
    for entry in db_budget_years:
        budget_years.append(LedgerYear(
            year_id=entry['year_id'],
            ledger_year=entry['ledger_year'],
            lid=entry['lid']
        ))
    
    return budget_years

def list_budget_entries(lid: int) -> list[BudgetEntry] | None:
    conn = db_connection()

    budget_entries = conn.execute(
        "SELECT * FROM budget_entries WHERE lid = ?",
        (lid,)
    ).fetchall()
    
    conn.close()

    if budget_entries is None:
        return None

    entries: list[BudgetEntry] = []
    for entry in budget_entries:
        entries.append(BudgetEntry(
            bid=entry['bid'],
            year_id=entry['year_id'],
            amount=entry['amount'],
            cid=entry['cid'],
            lid=entry['lid'],
            type_id=entry['type_id'],
            month=entry['month']
        ))
    
    return entries

def get_budget_entry(bid: int) -> BudgetEntry | None:
    conn = db_connection()
    db_entry = conn.execute(
        "SELECT * FROM budget_entries WHERE bid = ?",
        (bid,)
    ).fetchone()
    conn.close()

    if not db_entry:
        return None
    
    return BudgetEntry(
        bid=db_entry['bid'],
        year_id=db_entry['year_id'],
        amount=db_entry['amount'],
        cid=db_entry['cid'],
        lid=db_entry['lid'],
        type_id=db_entry['type_id'],
        month=db_entry['month']
    )

def insert_budget_entry(year_id: int, amount: float, cid: int, lid: int, type_id: int, month: int) -> int | None:
    conn = db_connection()
    cur = conn.execute(
        "INSERT INTO budget_entries (year_id, amount, cid, lid, type_id, month) VALUES (?, ?, ?, ?, ?, ?)",
        (year_id, amount, cid, lid, type_id, month)
    )
    conn.commit()
    entry_id = cur.lastrowid
    conn.close()
    return entry_id

def update_budget_entry(bid: int, amount: float) -> None:
    conn = db_connection()
    conn.execute(
        "UPDATE budget_entries SET amount = ? WHERE bid = ?",
        (amount, bid, )
    )
    conn.commit()
    conn.close()
    print(f"Budget entry {bid} updated")

def delete_budget_entry(bid: int) -> None:
    conn = db_connection()
    conn.execute("DELETE FROM budget_entries WHERE bid = ?", (bid,))
    conn.commit()
    conn.close()

def add_ledger_year(lid: int, year: int) -> None:
    conn = db_connection()
    conn.execute("INSERT OR IGNORE INTO ledger_years (ledger_year, lid) VALUES (?, ?)", (year,lid))
    conn.commit()
    conn.close()

def list_budget_entries_detailed(lid: int, year:int, month:int) -> list[BudgetEntryDetailed] | None:
    conn = db_connection()

    budget_entries = conn.execute(
        "SELECT * FROM budget_details WHERE lid = ? AND ledger_year = ? AND month = ?",
        (lid,year,month,)
    ).fetchall()
    
    conn.close()

    if budget_entries is None:
        return None

    entries: list[BudgetEntryDetailed] = []
    for entry in budget_entries:
        entries.append(BudgetEntryDetailed(
            bid=entry['bid'],
            year_id=entry['year_id'],
            amount=entry['amount'],
            cid=entry['cid'],
            lid=entry['lid'],
            type_id=entry['type_id'],
            month=entry['month'],
            type_name=entry["type_name"],
            category_name=entry["category_name"],
            ledger_year=entry["ledger_year"]
        ))
    
    return entries

def list_budget_entries_detailed_fullyear(lid: int, year:int) -> list[BudgetEntryDetailed] | None:
    conn = db_connection()

    budget_entries = conn.execute(
        """
            SELECT 
                SUM(amount) as amount, 
                bid,
                year_id,
                amount,
                cid,
                lid,
                type_id,
                type_name,
                category_name,
                ledger_year
            FROM 
                budget_details 
            WHERE lid = ? 
                AND ledger_year = ? 
            GROUP BY 
                ledger_year, 
                category_name
        """,
        (lid,year,)
    ).fetchall()
    
    conn.close()
 
    if budget_entries is None:
        return None

    entries: list[BudgetEntryDetailed] = []
    for entry in budget_entries:
        entries.append(BudgetEntryDetailed(
            bid=entry['bid'],
            year_id=entry['year_id'],
            amount=entry['amount'],
            cid=entry['cid'],
            lid=entry['lid'],
            type_id=entry['type_id'],
            month=None,
            type_name=entry["type_name"],
            category_name=entry["category_name"],
            ledger_year=entry["ledger_year"]
        ))
    
    return entries