import pandas as pd

def calculate_totals(df):

    income = df[df["type"] == "Income"]["amount"].sum()

    expenses = df[df["type"] == "Expense"]["amount"].sum()

    savings = income - expenses

    return income, expenses, savings

def category_summary(df):

    expenses = df[df["type"] == "Expense"]

    return expenses.groupby("category")["amount"].sum()

def monthly_summary(df):

    df["date"] = pd.to_datetime(df["date"])

    df["month"] = df["date"].dt.to_period("M")

    return df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)