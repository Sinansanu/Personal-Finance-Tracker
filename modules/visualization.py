import matplotlib.pyplot as plt

def expense_pie_chart(category_data):

    plt.figure(figsize=(6,6))

    category_data.plot(
        kind="pie",
        autopct="%1.1f%%"
    )

    plt.ylabel("")
    plt.title("Expenses by Category")

    plt.savefig("charts/pie_chart.png")

def monthly_bar_chart(monthly_data):

    monthly_data.plot(kind="bar", figsize=(8,5))

    plt.title("Monthly Income vs Expense")
    plt.ylabel("Amount")

    plt.savefig("charts/monthly_bar.png")

def savings_line_chart(monthly_data):

    savings = monthly_data["Income"] - monthly_data["Expense"]

    savings.plot(marker="o", figsize=(8,5))

    plt.title("Monthly Savings Trend")
    plt.ylabel("Savings")

    plt.savefig("charts/savings_line.png")