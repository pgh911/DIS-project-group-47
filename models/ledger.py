import sqlite3
from database import db_connection

class Ledger:
    def __init__(self, lid: int, ledger_name: str, user_id: int | None = None) -> None:
        self.lid: int = lid
        self.ledger_name: str = ledger_name
        self.user_id: int | None = user_id

class SummedTotal:
    def __init__(self, lid:int, category_name:str, type_name:str, posting_month:int, total_amount:float, posting_year:int):
        self.lid = lid
        self.category_name = category_name
        self.type_name = type_name
        self.posting_month = posting_month
        self.total_amount = total_amount
        self.posting_year = posting_year


def list_ledgers(user_id: int) -> list[Ledger]:
    conn = db_connection()
    db_ledgers = conn.execute(
        "SELECT * FROM ledgers WHERE user_id = ? ORDER BY lid",
        (user_id,)
    ).fetchall()
    conn.close()

    ledgers: list[Ledger] = []
    for db_ledger in db_ledgers:
        ledgers.append(Ledger(db_ledger['lid'], db_ledger['ledger_name'], db_ledger['user_id']))
    return ledgers


def get_ledger(lid: int) -> Ledger | None:
    conn = db_connection()
    db_ledger = conn.execute(
        "SELECT * FROM ledgers WHERE lid = ?",
        (lid,)
    ).fetchone()
    conn.close()

    if db_ledger:
        return Ledger(db_ledger['lid'], db_ledger['ledger_name'], db_ledger['user_id'])
    return None


def insert_ledger(user_id: int, ledger_name: str) -> int | None:
    conn = db_connection()
    cur = conn.execute(
        "INSERT INTO ledgers (user_id, ledger_name) VALUES (?, ?)",
        (user_id, ledger_name)
    )
    conn.commit()
    ledger_id = cur.lastrowid
    conn.close()
    return ledger_id


def update_ledger(lid: int, new_name: str) -> None:
    conn = db_connection()
    conn.execute(
        "UPDATE ledgers SET ledger_name = ? WHERE lid = ?",
        (new_name, lid)
    )
    conn.commit()
    conn.close()


def delete_ledger(lid: int) -> None:
    conn = db_connection()
    conn.execute("DELETE FROM ledgers WHERE lid = ?", (lid,))
    conn.commit()
    conn.close()

def get_summed_totals(
        lid: int, 
        year: int,
        month: int
        ) -> list[SummedTotal]:
    conn = db_connection()
    db_total = conn.execute(
        """
        SELECT
            *
        FROM posting_sum c
        WHERE c.lid = ?
        AND c.posting_month = ?
        AND c.posting_year = ?
        """,
        (lid,month,year,)
    ).fetchall()
    conn.close()

    summed_totals: list[SummedTotal] = []
    for entry in db_total:
        summed_totals.append(
            SummedTotal(
                lid=entry["lid"],
                category_name=entry["category_name"],
                type_name=entry["type_name"],
                posting_month=entry["posting_month"],
                posting_year=entry["posting_year"],
                total_amount=entry["total_amount"] 
            )
        )

    return summed_totals

def get_summed_totals_fullyear(
        lid: int, 
        year: int,
    ) -> list[sqlite3.Row]:
    conn = db_connection()
    db_total = conn.execute(
        """
        SELECT
            *
        FROM posting_sum c
        WHERE c.lid = ?
        AND c.posting_year = ?
        """,
        (lid,year,)
    ).fetchall()
    conn.close()

    summed_totals: list[SummedTotal] = []
    for entry in db_total:
        summed_totals.append(
            SummedTotal(
                lid=entry["lid"],
                category_name=entry["category_name"],
                type_name=entry["type_name"],
                posting_month=entry["posting_month"],
                posting_year=entry["posting_year"],
                total_amount=entry["total_amount"] 
            )
        )

    return summed_totals
