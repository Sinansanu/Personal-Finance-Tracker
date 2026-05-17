# Personal Finance Tracker

Personal Finance Tracker is a Python and Streamlit based application used to manage personal finances efficiently.  
It helps users track income and expenses, analyze spending habits, visualize financial data, forecast future savings, and generate downloadable reports.

---

## Features

- Add and manage financial transactions
- Track income and expenses
- Analyze financial summaries
- Forecast future savings
- Generate charts and visualizations
- Download PDF reports
- Download CSV transaction data

---

## Technologies Used

- Python
- Streamlit
- Pandas
- Matplotlib
- ReportLab
- NumPy

---

## Project Structure

```text
personal_finance_tracker/
│
├── app.py
├── transactions.csv
├── requirements.txt
│
├── assets/
│   └── logo.png
│
├── charts/
│
├── reports/
│
├── modules/
│   ├── transaction_manager.py
│   ├── data_analysis.py
│   ├── forecast.py
│   ├── visualization.py
│   └── report_generator.py
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Sinansanu/Personal-Finance-Tracker.git
```

### 2. Navigate to Project Folder

```bash
cd Personal-Finance-Tracker
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
streamlit run app.py
```

The application will run at:

```text
http://localhost:8501
```

---

## Generated Charts

- Expense Pie Chart
- Monthly Income vs Expense Bar Chart
- Savings Trend Line Chart

---

## Generated Reports

### PDF Report Includes:
- Financial Summary
- Forecast Summary
- Monthly Summary
- Category-wise Expenses
- Financial Charts

### CSV Export Includes:
- Complete transaction data

---

## Forecasting Methods

### Moving Average Forecast
Predicts future values based on recent averages.

### Trend-Based Forecast
Predicts future trends using historical growth patterns.

---

## Future Enhancements

- User Authentication
- Cloud Database Integration
- AI-Based Spending Insights
- Multi-Currency Support
- Investment Tracking

---

## References

- https://streamlit.io
- https://matplotlib.org
- https://www.reportlab.com
- https://pandas.pydata.org
- https://python.org