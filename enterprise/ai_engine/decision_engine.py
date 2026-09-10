import google.generativeai as genai

from config import GEMINI_API_KEY

from enterprise.services.sql_queries import (
    get_top_products,
    get_top_customers,
    get_monthly_sales,
    get_profit_by_category,
    get_city_customers,
    get_low_stock
)

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_business_ai(question):

    question = question.lower()

    if "product" in question:
        df = get_top_products()

    elif "customer" in question:
        df = get_top_customers()

    elif "month" in question or "sales" in question:
        df = get_monthly_sales()

    elif "profit" in question:
        df = get_profit_by_category()

    elif "city" in question:
        df = get_city_customers()

    elif "stock" in question or "inventory" in question:
        df = get_low_stock()

    else:
        return "Please ask about products, customers, sales, profit, city or inventory."

    table = df.to_string(index=False)

    prompt = f"""
You are a Senior Enterprise Business Consultant.

Business Data:

{table}

Question:

{question}

Provide:
1. Business Analysis
2. Insights
3. Recommendations
4. Next Action
"""

    response = model.generate_content(prompt)

    return response.text