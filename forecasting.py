"""Forecasting utilities using scikit-learn for next-month projections.

Provides linear regression-based forecasts with a simple average fallback
when data is insufficient. Does not print; returns structured results.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


@dataclass(frozen=True)
class ForecastResult:
    next_month: str  # 'YYYY-MM'
    method: str  # 'linear_regression' or 'average'
    predicted_expense: float
    predicted_income: float
    predicted_balance: float


def _prepare_monthly(df: pd.DataFrame) -> pd.DataFrame:
    tmp = df.copy()
    tmp["month"] = pd.to_datetime(tmp["date"]).dt.to_period("M").astype(str)
    grouped = tmp.groupby(["month", "type"], as_index=False)["amount"].sum()
    pivot = grouped.pivot(index="month", columns="type", values="amount").fillna(0.0)
    for col in ["Income", "Expense"]:
        if col not in pivot.columns:
            pivot[col] = 0.0
    pivot = pivot[["Income", "Expense"]]
    pivot.columns = ["income", "expense"]
    pivot["balance"] = pivot["income"] - pivot["expense"]
    pivot = pivot.reset_index()  # month, income, expense, balance
    return pivot


def _fit_or_average(series: pd.Series) -> tuple[float, str]:
    """Predict next value using linear regression; fallback to average/last.

    Returns (prediction, method).
    """
    y = series.astype(float).values
    n = len(y)
    if n == 0:
        return 0.0, "average"
    if n == 1:
        return float(max(0.0, y[0])), "average"

    # Linear regression on time index
    X = np.arange(n).reshape(-1, 1)
    model = LinearRegression()
    try:
        model.fit(X, y)
        y_pred = float(model.predict(np.array([[n]]))[0])  # next step
        if np.isfinite(y_pred):
            return max(0.0, y_pred), "linear_regression"
    except Exception:
        # Fall back below
        pass

    avg = float(np.mean(y))
    return max(0.0, avg), "average"


def _next_month_str(month_series: pd.Series) -> str:
    if len(month_series) == 0:
        # Use current calendar next month when no data
        last = pd.Timestamp.today().to_period("M")
    else:
        last = pd.Period(str(month_series.iloc[-1]), freq="M")
    nxt = last + 1
    return str(nxt)


def forecast_next_month(df: pd.DataFrame) -> ForecastResult:
    """Forecast next month income, expense, and balance.

    Parameters
    ----------
    df: pd.DataFrame
        Transactions DataFrame with at least ['date','type','amount'].

    Returns
    -------
    ForecastResult
        Contains predicted values and the method used.
    """
    if df is None or df.empty:
        next_month = _next_month_str(pd.Series([], dtype=str))
        return ForecastResult(
            next_month=next_month,
            method="average",
            predicted_expense=0.0,
            predicted_income=0.0,
            predicted_balance=0.0,
        )

    monthly = _prepare_monthly(df)
    income_pred, method_inc = _fit_or_average(monthly["income"])  # noqa: F841
    expense_pred, method_exp = _fit_or_average(monthly["expense"])  # noqa: F841

    # Prefer linear regression if either used it; else average
    method = "linear_regression" if (method_inc == "linear_regression" or method_exp == "linear_regression") else "average"

    predicted_income = round(income_pred, 2)
    predicted_expense = round(expense_pred, 2)
    predicted_balance = round(predicted_income - predicted_expense, 2)

    next_month = _next_month_str(monthly["month"])  # type: ignore[arg-type]

    return ForecastResult(
        next_month=next_month,
        method=method,
        predicted_expense=predicted_expense,
        predicted_income=predicted_income,
        predicted_balance=predicted_balance,
    )
