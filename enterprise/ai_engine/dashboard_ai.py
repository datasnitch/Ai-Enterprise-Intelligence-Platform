import google.generativeai as genai

from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def dashboard_recommendation(

    total_sales,
    total_profit,
    profit_margin,
    total_orders,
    total_customers

):

    prompt = f"""
You are a Senior Business Consultant.

Business KPIs

Revenue: {total_sales}

Profit: {total_profit}

Profit Margin: {profit_margin:.2f}%

Orders: {total_orders}

Customers: {total_customers}

Give:

1. Executive Summary

2. Key Insights

3. Risks

4. Recommendations

Keep it under 200 words.
"""

    response = model.generate_content(prompt)

    return response.text