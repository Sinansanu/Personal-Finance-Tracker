"""Transaction management using SQLite for Personal Finance Tracker.

This module provides functions to create and manage a SQLite-backed
transaction store. It exposes a pandas-friendly loader so downstream
modules can analyze and visualize the data.

Public functions:
- init_db
- add_transaction
- edit_transaction
- delete_transaction
- load_transactions

A transaction row has the following fields:
- id: INTEGER PRIMARY KEY
- date: TEXT (YYYY-MM-DD)
- ttype: TEXT ('Income' or 'Expense')
- category: TEXT
- amount: REAL (>= 0)
- notes: TEXT (optional)
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional
import sqlite3

import pandas as pd

# Default database path inside the project data directory
DEFAULT_DB_PATH: Path = Path(__file__).resolve().parent / "data" / "transactions.db"


def init_db(db_path: str | Path = DEFAULT_DB_PATH) -> None:
    """Initialize the SQLite database and ensure the schema exists.

    Parameters
    ----------
    db_path: str | Path
        Path to the SQLite database file. Parent directories are created
        when needed.
    """
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                ttype TEXT NOT NULL CHECK (ttype IN ('Income','Expense')),
                category TEXT NOT NULL,
                amount REAL NOT NULL CHECK (amount >= 0),
                notes TEXT
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date)"
        )
        conn.commit()


def _normalize_date(date_value: str | datetime) -> str:
    """Normalize various date representations to 'YYYY-MM-DD' string."""
    if isinstance(date_value, datetime):
        return date_value.strftime("%Y-%m-%d")
    # pandas handles many string formats robustly
    return pd.to_datetime(date_value).strftime("%Y-%m-%d")


def _validate_transaction_type(transaction_type: str) -> str:
    t = transaction_type.strip().title()
    if t not in {"Income", "Expense"}:
        raise ValueError("transaction_type must be 'Income' or 'Expense'")
    return t


def add_transaction(
    date: str | datetime,
    transaction_type: str,
    category: str,
    amount: float,
    notes: Optional[str] = None,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> int:
    """Insert a new transaction and return its generated ID.

    Parameters
    ----------
    date: str | datetime
        Date of the transaction; flexible input, stored as YYYY-MM-DD.
    transaction_type: str
        Either 'Income' or 'Expense'.
    category: str
        Category name such as 'Salary', 'Food', 'Rent'.
    amount: float
        Non-negative transaction amount. For expenses use positive values.
    notes: Optional[str]
        Optional free-text notes.
    db_path: str | Path
        SQLite database path.
    """
    if amount < 0:
        raise ValueError("amount must be non-negative")
    ttype = _validate_transaction_type(transaction_type)
    date_str = _normalize_date(date)

    with sqlite3.connect(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO transactions(date, ttype, category, amount, notes) VALUES (?,?,?,?,?)",
            (date_str, ttype, category.strip(), float(amount), notes),
        )
        conn.commit()
        return int(cur.lastrowid)


def edit_transaction(
    transaction_id: int,
    *,
    date: Optional[str | datetime] = None,
    transaction_type: Optional[str] = None,
    category: Optional[str] = None,
    amount: Optional[float] = None,
    notes: Optional[str] = None,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> bool:
    """Update an existing transaction. Returns True if a row was updated.

    Only provided fields are updated.
    """
    fields: list[str] = []
    values: list[object] = []

    if date is not None:
        fields.append("date = ?")
        values.append(_normalize_date(date))
    if transaction_type is not None:
        fields.append("ttype = ?")
        values.append(_validate_transaction_type(transaction_type))
    if category is not None:
        fields.append("category = ?")
        values.append(category.strip())
    if amount is not None:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        fields.append("amount = ?")
        values.append(float(amount))
    if notes is not None:
        fields.append("notes = ?")
        values.append(notes)

    if not fields:
        return False

    values.append(transaction_id)

    with sqlite3.connect(db_path) as conn:
        cur = conn.execute(
            f"UPDATE transactions SET {', '.join(fields)} WHERE id = ?",
            values,
        )
        conn.commit()
        return cur.rowcount > 0


def delete_transaction(transaction_id: int, db_path: str | Path = DEFAULT_DB_PATH) -> bool:
    """Delete a transaction by ID. Returns True if a row was deleted."""
    with sqlite3.connect(db_path) as conn:
        cur = conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        return cur.rowcount > 0


def load_transactions(db_path: str | Path = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Load all transactions as a pandas DataFrame.

    Returns columns: ['id', 'date', 'type', 'category', 'amount', 'notes']
    with 'date' as pandas datetime64[ns].
    """
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(
            "SELECT id, date, ttype AS type, category, amount, notes FROM transactions ORDER BY date, id",
            conn,
        )
    if df.empty:
        return pd.DataFrame(
            columns=["id", "date", "type", "category", "amount", "notes"]
        )
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df
