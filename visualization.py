"""Visualization utilities using matplotlib for Personal Finance Tracker.

Generates and saves plots to PNG files without showing interactive windows.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use("Agg")  # non-interactive backend for headless environments
import matplotlib.pyplot as plt
import pandas as pd

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def _prepare_output_dir(output_dir: str | Path | None) -> Path:
    path = Path(output_dir) if output_dir is not None else DEFAULT_OUTPUT_DIR
    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_charts(
    df: pd.DataFrame,
    monthly_summary: pd.DataFrame,
    expense_by_category: pd.DataFrame,
    output_dir: Optional[str | Path] = None,
) -> dict:
    """Create pie, line, and bar charts saved as PNG files.

    Returns a dict with file paths for the generated charts.
    """
    out_dir = _prepare_output_dir(output_dir)
    outputs = {}

    # Pie chart: expenses by category
    pie_path = out_dir / "expenses_by_category.png"
    if expense_by_category is not None and not expense_by_category.empty:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            expense_by_category["expense"],
            labels=expense_by_category["category"],
            autopct="%1.1f%%",
            startangle=140,
        )
        ax.set_title("Expenses by Category")
        plt.tight_layout()
        fig.savefig(pie_path, dpi=150)
        plt.close(fig)
    else:
        # Create an empty placeholder plot
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.text(0.5, 0.5, "No expense data", ha="center", va="center")
        ax.axis("off")
        fig.savefig(pie_path, dpi=150)
        plt.close(fig)
    outputs["pie_expenses_by_category"] = str(pie_path)

    # Line chart: monthly balance trend
    line_path = out_dir / "monthly_balance_trend.png"
    if monthly_summary is not None and not monthly_summary.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(monthly_summary["month"], monthly_summary["balance"], marker="o")
        ax.set_title("Monthly Balance Trend")
        ax.set_xlabel("Month")
        ax.set_ylabel("Balance")
        ax.grid(True, linestyle=":", linewidth=0.5)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        fig.savefig(line_path, dpi=150)
        plt.close(fig)
    else:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "No monthly data", ha="center", va="center")
        ax.axis("off")
        fig.savefig(line_path, dpi=150)
        plt.close(fig)
    outputs["line_monthly_balance_trend"] = str(line_path)

    # Bar chart: income vs expenses per month
    bar_path = out_dir / "income_vs_expenses.png"
    if monthly_summary is not None and not monthly_summary.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        x = range(len(monthly_summary))
        ax.bar(x, monthly_summary["income"], width=0.4, label="Income")
        ax.bar([i + 0.4 for i in x], monthly_summary["expense"], width=0.4, label="Expense")
        ax.set_title("Income vs Expenses")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount")
        ax.set_xticks([i + 0.2 for i in x], monthly_summary["month"], rotation=45, ha="right")
        ax.legend()
        ax.grid(True, axis="y", linestyle=":", linewidth=0.5)
        plt.tight_layout()
        fig.savefig(bar_path, dpi=150)
        plt.close(fig)
    else:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "No monthly data", ha="center", va="center")
        ax.axis("off")
        fig.savefig(bar_path, dpi=150)
        plt.close(fig)
    outputs["bar_income_vs_expenses"] = str(bar_path)

    return outputs
