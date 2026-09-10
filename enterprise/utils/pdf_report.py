from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from reportlab.lib.styles import getSampleStyleSheet

from enterprise.ai_engine.executive_summary import generate_summary


def generate_pdf(
    filename,
    total_sales,
    total_profit,
    profit_margin,
    total_orders,
    total_customers,
    total_products
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    # ==========================================
    # Title
    # ==========================================

    story.append(
        Paragraph(
            "<b>AI Enterprise Intelligence Platform</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Executive Business Report</b>",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 20))

    # ==========================================
    # KPI Section
    # ==========================================

    story.append(
        Paragraph(
            f"<b>Total Revenue:</b> ₹{total_sales:,.0f}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Total Profit:</b> ₹{total_profit:,.0f}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Profit Margin:</b> {profit_margin:.2f}%",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Total Orders:</b> {total_orders}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Total Customers:</b> {total_customers}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Total Products:</b> {total_products}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    # ==========================================
    # Business Health
    # ==========================================

    story.append(
        Paragraph(
            "<b>Business Health</b>",
            styles["Heading2"]
        )
    )

    if profit_margin >= 25:

        health = "Excellent Business Performance"

    elif profit_margin >= 15:

        health = "Business Performance is Stable"

    else:

        health = "Business Needs Improvement"

    story.append(
        Paragraph(
            health,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    # ==========================================
    # AI Executive Summary
    # ==========================================

    story.append(
        Paragraph(
            "<b>AI Executive Summary</b>",
            styles["Heading2"]
        )
    )

    summary = generate_summary(
        total_sales,
        total_profit,
        profit_margin,
        total_orders,
        total_customers
    )

    story.append(
        Paragraph(
            summary.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    # ==========================================
    # Build PDF
    # ==========================================

    doc.build(story)