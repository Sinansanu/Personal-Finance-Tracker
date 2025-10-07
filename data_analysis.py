"""Data analysis utilities for Personal Finance Tracker.

Computes aggregate metrics and monthly/category summaries without printing.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

import pandas as pd


@dataclass(frozen=True)
class AnalysisResult:
    """Structured result for downstream consumption and exports."""
    totals: Dict[str, float]
    monthly_summary: pd.DataFrame  # columns: month, income, expense, balance
    expense_by_category: pd.DataFrame  # columns: category, expense


def _ensure_expected_columns(df: pd.DataFrame) -> None:
    required = {"date", "type", "category", "amount"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def _compute_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    temp = df.copy()
    temp["month"] = pd.to_datetime(temp["date"]).dt.to_period("M").astype(str)
    grouped = (
        temp.groupby(["month", "type"], as_index=False)["amount"].sum()
    )
    pivot = grouped.pivot(index="month", columns="type", values="amount").fillna(0.0)
    # Normalize column names to lower-case
    for col in ["Income", "Expense"]:
        if col not in pivot.columns:
            pivot[col] = 0.0
    pivot = pivot[["Income", "Expense"]]
    pivot.columns = ["income", "expense"]
    pivot["balance"] = pivot["income"] - pivot["expense"]
    pivot = pivot.reset_index()
    return pivot  # month, income, expense, balance


def analyze_data(df: pd.DataFrame) -> AnalysisResult:
    """Compute totals and summaries.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame with columns ['id','date','type','category','amount','notes'].

    Returns
    -------
    AnalysisResult
        Contains totals, monthly summary, and expense-by-category totals.
    """
    if df is None or df.empty:
        empty_monthly = pd.DataFrame(columns=["month", "income", "expense", "balance"])
        empty_cat = pd.DataFrame(columns=["category", "expense"])
        totals = {"total_income": 0.0, "total_expenses": 0.0, "net_savings": 0.0}
        return AnalysisResult(totals=totals, monthly_summary=empty_monthly, expense_by_category=empty_cat)

    _ensure_expected_columns(df)

    total_income = float(df.loc[df["type"] == "Income", "amount"].sum())
    total_expenses = float(df.loc[df["type"] == "Expense", "amount"].sum())
    net_savings = total_income - total_expenses

    monthly_summary = _compute_monthly_summary(df)

    expense_by_category = (
        df[df["type"] == "Expense"]
        .groupby("category", as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "expense"})
        .sort_values("expense", ascending=False)
        .reset_index(drop=True)
    )

    totals = {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_savings": round(net_savings, 2),
    }

    return AnalysisResult(
        totals=totals,
        monthly_summary=monthly_summary,
        expense_by_category=expense_by_category,
    )
