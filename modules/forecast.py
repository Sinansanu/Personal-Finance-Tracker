import numpy as np

def moving_average(values, window=3):

    if len(values) < window:
        return np.mean(values)

    return np.mean(values[-window:])

def trend_forecast(values):

    if len(values) < 2:
        return values[-1]

    changes = []

    for i in range(1, len(values)):
        changes.append(values[i] - values[i - 1])

    avg_change = np.mean(changes)

    return values[-1] + avg_change

def generate_forecast(income_list, expense_list):

    income_ma = moving_average(income_list)
    expense_ma = moving_average(expense_list)

    income_trend = trend_forecast(income_list)
    expense_trend = trend_forecast(expense_list)

    savings_ma = income_ma - expense_ma
    savings_trend = income_trend - expense_trend

    return {
        "Income MA": income_ma,
        "Expense MA": expense_ma,
        "Savings MA": savings_ma,
        "Income Trend": income_trend,
        "Expense Trend": expense_trend,
        "Savings Trend": savings_trend
    }