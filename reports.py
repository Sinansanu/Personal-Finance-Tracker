"""Report export utilities for Personal Finance Tracker.

Exports analysis and forecast summaries to CSV and JSON files.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, Optional

import pandas as pd

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def _prepare_output_dir(output_dir: Optional[str | Path]) -> Path:
    path = Path(output_dir) if output_dir is not None else DEFAULT_OUTPUT_DIR
    path.mkdir(parents=True, exist_ok=True)
    return path


def export_reports(
    summary_totals: Dict[str, float],
    monthly_summary: pd.DataFrame,
    expense_by_category: pd.DataFrame,
    forecast: Dict[str, Any],
    output_dir: Optional[str | Path] = None,
) -> Dict[str, str]:
    """Export the summary and forecast to disk.

    Writes:
    - summary.csv (totals row + monthly summary appended below)
    - forecast.json
    - expense_by_category.csv

    Returns paths of the generated files.
    """
    out_dir = _prepare_output_dir(output_dir)

    # Write summary.csv with totals then monthly breakdown
    summary_csv = out_dir / "summary.csv"
    totals_df = pd.DataFrame([summary_totals])
    totals_df["section"] = "totals"

    monthly_df = monthly_summary.copy()
    monthly_df["section"] = "monthly"

    combined = pd.concat([totals_df, monthly_df], ignore_index=True, sort=False)
    combined.to_csv(summary_csv, index=False)

    # Write expense_by_category.csv
    by_cat_csv = out_dir / "expense_by_category.csv"
    expense_by_category.to_csv(by_cat_csv, index=False)

    # Write forecast.json
    forecast_json = out_dir / "forecast.json"
    with open(forecast_json, "w", encoding="utf-8") as f:
        json.dump(forecast, f, indent=2)

    return {
        "summary_csv": str(summary_csv),
        "expense_by_category_csv": str(by_cat_csv),
        "forecast_json": str(forecast_json),
    }
