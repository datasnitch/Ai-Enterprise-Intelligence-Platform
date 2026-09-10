import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def executive_ai(
    total_sales,
    total_profit,
    profit_margin,
    total_orders,
    total_customers,
    total_products,
):

    prompt = f"""
You are a Senior Enterprise Strategy Consultant.

Analyze the business below.

Revenue:
{total_sales}

Profit:
{total_profit}

Profit Margin:
{profit_margin:.2f}%

Orders:
{total_orders}

Customers:
{total_customers}

Products:
{total_products}

Generate a professional report.

Include:

1. Executive Summary

2. Business Health

3. SWOT Analysis

Strengths

Weaknesses

Opportunities

Threats

4. Business Risks

5. Strategic Recommendations

6. Next Quarter Action Plan

7. CEO Final Recommendation

Write professionally.

Use headings.

Do not use markdown tables.
"""

    response = model.generate_content(prompt)

    return response.text