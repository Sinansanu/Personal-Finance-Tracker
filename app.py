import streamlit as st

from modules.transaction_manager import *
from modules.data_analysis import *
from modules.forecast import *
from modules.visualization import *
from modules.report_generator import *

st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="assets/logo.png",
    layout="wide"
)

col1, col2 = st.columns([1, 6])

with col1:
    st.image(
        "assets/logo.png",
        width=110
    )

with col2:
    st.markdown(
        """
        # Personal Finance Tracker
        ### Track • Analyze • Forecast
        """
    )

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Transaction",
        "View Transactions",
        "Analysis",
        "Forecast",
        "Generate Report"
    ]
)

# ADD TRANSACTION
if menu == "Add Transaction":

    st.header("Add Transaction")

    date = st.date_input("Date")

    t_type = st.selectbox(
        "Type",
        ["Income", "Expense"]
    )

    category = st.selectbox(
        "Category",
        [
            "Salary",
            "Freelance",
            "Investment",
            "Groceries",
            "Transport",
            "Food",
            "Entertainment",
            "Utilities",
            "Shopping",
            "Healthcare",
            "Education",
            "Rent",
            "Travel",
            "Internet",
            "Other"
        ]
    )

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=100.0
    )

    notes = st.text_area("Notes")

    if st.button("Add Transaction"):

        add_transaction(
            str(date),
            t_type,
            category,
            amount,
            notes
        )

        st.success("Transaction Added Successfully")

# VIEW TRANSACTIONS
elif menu == "View Transactions":

    st.header("All Transactions")

    df = view_transactions()

    st.dataframe(
        df,
        use_container_width=True
    )

# ANALYSIS
elif menu == "Analysis":

    st.header("Financial Analysis")

    df = view_transactions()

    if df.empty:

        st.warning("No transactions available.")

    else:

        income, expenses, savings = calculate_totals(df)

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Income", f"₹{income:,.2f}")
        col2.metric("Total Expenses", f"₹{expenses:,.2f}")
        col3.metric("Net Savings", f"₹{savings:,.2f}")

        category = category_summary(df)

        monthly = monthly_summary(df)

        # Generate Charts
        expense_pie_chart(category)
        monthly_bar_chart(monthly)
        savings_line_chart(monthly)

        st.subheader("Expense Distribution")

        st.image(
            "charts/pie_chart.png",
            use_container_width=True
        )

        st.subheader("Monthly Income vs Expense")

        st.image(
            "charts/monthly_bar.png",
            use_container_width=True
        )

        st.subheader("Savings Trend")

        st.image(
            "charts/savings_line.png",
            use_container_width=True
        )

# FORECAST
elif menu == "Forecast":

    st.header("Financial Forecast")

    df = view_transactions()

    if df.empty:

        st.warning("No transactions available.")

    else:

        monthly = monthly_summary(df)

        income_list = monthly["Income"].tolist()

        expense_list = monthly["Expense"].tolist()

        result = generate_forecast(
            income_list,
            expense_list
        )

        st.subheader("Forecast Summary")

        for key, value in result.items():

            st.write(
                f"**{key}:** ₹{value:,.2f}"
            )

# GENERATE REPORT
elif menu == "Generate Report":

    st.header("Generate Financial Report")

    df = view_transactions()

    if df.empty:

        st.warning("No transactions available.")

    else:

        income, expenses, savings = calculate_totals(df)

        summary = {
            "Income": income,
            "Expenses": expenses,
            "Savings": savings
        }

        category = category_summary(df)

        monthly = monthly_summary(df)

        # Generate Charts
        expense_pie_chart(category)
        monthly_bar_chart(monthly)
        savings_line_chart(monthly)

        income_list = monthly["Income"].tolist()

        expense_list = monthly["Expense"].tolist()

        forecast = generate_forecast(
            income_list,
            expense_list
        )

        # Generate PDF Report
        generate_pdf_report(
            summary,
            forecast,
            monthly,
            category
        )

        st.success("PDF Report Generated Successfully")

        # PDF DOWNLOAD
        with open(
            "reports/finance_report.pdf",
            "rb"
        ) as pdf_file:

            st.download_button(
                label="⬇ Download PDF Report",
                data=pdf_file,
                file_name="finance_report.pdf",
                mime="application/pdf"
            )

        # CSV DOWNLOAD
        csv = df.to_csv(index=False)

        st.download_button(
            label="⬇ Download CSV Data",
            data=csv,
            file_name="transactions.csv",
            mime="text/csv"
        )