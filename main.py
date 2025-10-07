"""Personal Finance Tracker with Forecast

Course: ICS214 – IT Workshop III
Guide: Dr. Cinu C. Kiliroor
Author: Mohammed Sinan (Roll No: 2024BCS0328)

This backend-only script wires together the project modules to:
- initialize storage
- seed sample transactions (no user I/O)
- analyze data
- forecast next month
- generate charts
- export reports
- return a final summary dictionary (also useful for tests)

Run this module directly to execute the end-to-end pipeline.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, Any

import pandas as pd

from transaction_manager import init_db, add_transaction, edit_transaction, delete_transaction, load_transactions, DEFAULT_DB_PATH
from data_analysis import analyze_data
from forecasting import forecast_next_month
from visualization import generate_charts
from reports import export_reports

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def seed_sample_data() -> None:
    """Seed sample transactions for demonstration and testing.

    This function is deterministic and idempotent at month boundaries
    by clearing existing rows in the small demo run to avoid duplicates.
    """
    # Reset database for a clean demo
    if DEFAULT_DB_PATH.exists():
        DEFAULT_DB_PATH.unlink()
    init_db(DEFAULT_DB_PATH)

    # Simulate several months of income and expenses
    # Use the first day of each month for consistency
    base_dates = pd.date_range("2024-01-01", periods=9, freq="MS").to_pydatetime().tolist()

    # Add monthly salary income
    for d in base_dates:
        add_transaction(d, "Income", "Salary", 50000.0, notes="Monthly salary")

    # Add varying expenses: Rent, Food, Utilities, Entertainment
    for i, d in enumerate(base_dates):
        add_transaction(d, "Expense", "Rent", 15000.0, notes="Monthly rent")
        add_transaction(d, "Expense", "Food", 6000.0 + (i * 150), notes="Groceries and dining")
        add_transaction(d, "Expense", "Utilities", 3000.0 + (i * 50), notes="Electricity, water, internet")
        add_transaction(d, "Expense", "Entertainment", 2000.0 + (i * 100), notes="Movies, outings")

    # One-time bonus in June
    add_transaction(datetime(2024, 6, 1), "Income", "Bonus", 10000.0, notes="Performance bonus")



def run_pipeline() -> Dict[str, Any]:
    """Execute the complete analysis and forecasting pipeline.

    Returns a summary dictionary with file paths of outputs.
    """
    init_db(DEFAULT_DB_PATH)

    # If empty, seed demo data
    df = load_transactions(DEFAULT_DB_PATH)
    if df.empty:
        seed_sample_data()
        df = load_transactions(DEFAULT_DB_PATH)

    # Analyze
    analysis = analyze_data(df)

    # Forecast
    forecast = forecast_next_month(df)

    # Visualize
    chart_paths = generate_charts(
        df=df,
        monthly_summary=analysis.monthly_summary,
        expense_by_category=analysis.expense_by_category,
        output_dir=OUTPUT_DIR,
    )

    # Export reports
    forecast_dict = {
        "next_month": forecast.next_month,
        "method": forecast.method,
        "predicted_income": forecast.predicted_income,
        "predicted_expense": forecast.predicted_expense,
        "predicted_balance": forecast.predicted_balance,
    }

    report_paths = export_reports(
        summary_totals=analysis.totals,
        monthly_summary=analysis.monthly_summary,
        expense_by_category=analysis.expense_by_category,
        forecast=forecast_dict,
        output_dir=OUTPUT_DIR,
    )

    final_summary: Dict[str, Any] = {
        "totals": analysis.totals,
        "forecast": forecast_dict,
        "charts": chart_paths,
        "reports": report_paths,
        "num_transactions": int(len(df)),
        "db_path": str(DEFAULT_DB_PATH),
    }
    return final_summary


if __name__ == "__main__":
    # Execute the pipeline; do not print to stdout per requirements.
    _ = run_pipeline()
