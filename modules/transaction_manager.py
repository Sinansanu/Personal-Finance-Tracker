import pandas as pd
import os

FILE = "transactions.csv"

def load_transactions():
    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=[
            "date", "type", "category", "amount", "notes"
        ])
        df.to_csv(FILE, index=False)

    return pd.read_csv(FILE)

def add_transaction(date, t_type, category, amount, notes):
    df = load_transactions()

    new_data = {
        "date": date,
        "type": t_type,
        "category": category,
        "amount": amount,
        "notes": notes
    }

    df.loc[len(df)] = new_data
    df.to_csv(FILE, index=False)

def delete_transaction(index):
    df = load_transactions()
    df = df.drop(index)
    df.to_csv(FILE, index=False)

def view_transactions():
    return load_transactions()