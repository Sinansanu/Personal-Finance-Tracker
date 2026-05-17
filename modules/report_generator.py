from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus.flowables import HRFlowable


def create_table(data, header_color):

    table = Table(
        data,
        colWidths=[220, 220]
    )

    table.setStyle(TableStyle([

        # Header
        ("BACKGROUND", (0, 0), (-1, 0), header_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),

        # Body
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 10),

        # Alignment
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        # Grid
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),

        # Padding
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("TOPPADDING", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 8),

    ]))

    return table


def generate_pdf_report(
    summary,
    forecast,
    monthly_data,
    category_data
):

    doc = SimpleDocTemplate(
        "reports/finance_report.pdf",
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    elements = []

    title_style = styles["Title"]

    elements.append(
        Image(
            "assets/logo.png",
            width=90,
            height=90
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            "Personal Finance Report",
            title_style
        )
    )
    
    

    elements.append(Spacer(1, 10))

    elements.append(
        HRFlowable(
            width="100%",
            thickness=2,
            color=colors.darkblue
        )
    )

    elements.append(Spacer(1, 25))

    elements.append(
        Paragraph(
            "<b>Financial Summary</b>",
            styles["Heading1"]
        )
    )

    elements.append(Spacer(1, 12))

    summary_table = [
        ["Metric", "Amount"],
        ["Total Income", f"₹ {summary['Income']:,.2f}"],
        ["Total Expenses", f"₹ {summary['Expenses']:,.2f}"],
        ["Net Savings", f"₹ {summary['Savings']:,.2f}"]
    ]

    elements.append(
        create_table(
            summary_table,
            colors.darkgreen
        )
    )

    elements.append(Spacer(1, 30))

    elements.append(
        Paragraph(
            "<b>Forecast Summary</b>",
            styles["Heading1"]
        )
    )

    elements.append(Spacer(1, 12))

    forecast_table = [
        ["Forecast Type", "Predicted Amount"]
    ]

    for key, value in forecast.items():

        forecast_table.append([
            key,
            f"₹ {value:,.2f}"
        ])

    elements.append(
        create_table(
            forecast_table,
            colors.darkorange
        )
    )

    elements.append(Spacer(1, 30))

    elements.append(
        Paragraph(
            "<b>Monthly Financial Summary</b>",
            styles["Heading1"]
        )
    )

    elements.append(Spacer(1, 12))

    monthly_table = [
        ["Month", "Income", "Expense"]
    ]

    for month, row in monthly_data.iterrows():

        monthly_table.append([
            str(month),
            f"₹ {row.get('Income', 0):,.0f}",
            f"₹ {row.get('Expense', 0):,.0f}"
        ])

    elements.append(
        create_table(
            monthly_table,
            colors.darkblue
        )
    )

    elements.append(Spacer(1, 30))

    elements.append(
        Paragraph(
            "<b>Category-wise Expenses</b>",
            styles["Heading1"]
        )
    )

    elements.append(Spacer(1, 12))

    category_table = [
        ["Category", "Expense Amount"]
    ]

    for category, amount in category_data.items():

        category_table.append([
            category,
            f"₹ {amount:,.0f}"
        ])

    elements.append(
        create_table(
            category_table,
            colors.purple
        )
    )

    elements.append(PageBreak())

    elements.append(
        Paragraph(
            "📊 Financial Charts & Visualization",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 15))

    elements.append(
        HRFlowable(
            width="100%",
            thickness=2,
            color=colors.darkred
        )
    )

    elements.append(Spacer(1, 25))

    elements.append(
        Paragraph(
            "<b>Expense Distribution by Category</b>",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Image(
            "charts/pie_chart.png",
            width=340,
            height=340
        )
    )

    elements.append(Spacer(1, 25))

    elements.append(
        Paragraph(
            "<b>Monthly Income vs Expense Comparison</b>",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Image(
            "charts/monthly_bar.png",
            width=450,
            height=250
        )
    )

    elements.append(Spacer(1, 25))

    elements.append(
        Paragraph(
            "<b>Monthly Savings Trend</b>",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Image(
            "charts/savings_line.png",
            width=450,
            height=250
        )
    )

    elements.append(Spacer(1, 25))

    elements.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.grey
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            "Generated using Personal Finance Tracker System",
            styles["Italic"]
        )
    )

    doc.build(elements)