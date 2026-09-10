import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import os
from datetime import datetime

from config import GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")
from enterprise.auth.login import login
from io import BytesIO
from enterprise.utils.pdf_report import generate_pdf
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet
from enterprise.ai_engine.dashboard_ai import dashboard_recommendation
from enterprise.ai_engine.executive_ai import executive_ai

def load_css():
    try:
        with open("enterprise/assets/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass



# --------------------------------------------
# Login Session
# --------------------------------------------

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "user" not in st.session_state:

    st.session_state.user = ""

if "role" not in st.session_state:

    st.session_state.role=""



# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="AI Enterprise Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

load_css()

# ==========================================
# Activity Logger
# ==========================================

def log_activity(activity):

    log_file = "logs/activity_log.csv"

    if not os.path.exists(log_file):

        with open(log_file, "w") as f:

            f.write("Timestamp,User,Role,Activity\n")

    with open(log_file, "a") as f:

        f.write(
            f"{datetime.now()},"
            f"{st.session_state.user},"
            f"{st.session_state.role},"
            f"{activity}\n"
        )



# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

@st.cache_data
def load_data():

    orders = pd.read_csv("data/cleaned/orders_clean.csv")
    customers = pd.read_csv("data/cleaned/customers_clean.csv")
    products = pd.read_csv("data/cleaned/products_clean.csv")
    inventory = pd.read_csv("data/cleaned/inventory_clean.csv")
    marketing = pd.read_csv("data/cleaned/marketing_clean.csv")
    employees = pd.read_csv("data/cleaned/employees_clean.csv")

    return (
        orders,
        customers,
        products,
        inventory,
        marketing,
        employees
    )


try:

    (
        orders,
        customers,
        products,
        inventory,
        marketing,
        employees
    ) = load_data()

except:

    st.error("Cleaned dataset not found.")

    st.stop()
# --------------------------------------------
# Authentication
# --------------------------------------------

if not st.session_state.logged_in:

    login()
    log_activity("User Logged In")

    st.stop()

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

st.sidebar.markdown("""

# 🏢 AI Enterprise

### Intelligence Platform

Enterprise Analytics

Version 2.0

""")

st.sidebar.success(

f"""

👤 {st.session_state.user}

Role

{st.session_state.role}

"""

)

if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False
    st.session_state.user = ""
    st.session_state.role = ""

    st.rerun()

if st.session_state.role=="Admin":

    pages=[

        "🏠 Home",

        "📊 Dashboard",

        "📈 Forecast",

        "👥 Customers",

        "📦 Inventory",

        "🤖 AI Assistant",

        "📄 Reports",

        "📜 Audit Log",

        "⚙ Settings"

    ]

elif st.session_state.role=="Manager":

    pages=[

        "🏠 Home",

        "📊 Dashboard",

        "📈 Forecast",

        "👥 Customers",

        "📦 Inventory",

        "🤖 AI Assistant"

    ]

else:

    pages=[

        "🏠 Home",

        "📊 Dashboard",

        "📈 Forecast"

    ]

page=st.sidebar.radio(

"Navigation",

pages

)


# ====================================================
# HOME
# ====================================================

if page == "🏠 Home":

    st.title("🏢 AI Enterprise Intelligence Platform")

    st.markdown("---")

    st.write(
        """
Welcome to the AI Enterprise Intelligence Platform.

This application provides:

- 📈 Sales Analytics
- 💰 Profit Analytics
- 👥 Customer Analytics
- 📦 Inventory Monitoring
- 🔮 Sales Forecasting
- 🤖 AI Business Assistant
"""
    )

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    c1.success("📊 Executive Dashboard")

    c2.info("🤖 Machine Learning")

    c3.warning("📈 Forecasting")

    # ==========================================
    # Customer Distribution
    # ==========================================

    city_count = (
    customers["City"]
    .value_counts()
    .reset_index()
    )

    city_count.columns = [
    "City",
    "Customers"
    ]

    fig4 = px.bar(
    city_count,
    x="City",
    y="Customers",
    color="Customers",
    title="Customers by City"
    )

    st.plotly_chart(
    fig4,
    use_container_width=True
    )

# ====================================================
# DASHBOARD
# ====================================================

elif page == "📊 Dashboard":

    st.title("📊 Executive Business Dashboard")
    log_activity("Viewed Dashboard")

    st.markdown("---")

    # ==========================================
    # Dashboard Filters
    # ==========================================

    st.subheader("🎯 Dashboard Filters")

    col1, col2, col3 = st.columns(3)

    selected_city = col1.selectbox(
    "City",
    ["All"] + sorted(customers["City"].unique().tolist())
    )

    selected_category = col2.selectbox(
    "Category",
    ["All"] + sorted(products["Category"].unique().tolist())
    )

    selected_warehouse = col3.selectbox(
    "Warehouse",
    ["All"] + sorted(inventory["Warehouse"].unique().tolist())
    )

    merged = orders.merge(products, on="ProductID")
    merged = merged.merge(customers, on="CustomerID")

    if selected_city != "All":
        merged = merged[
        merged["City"] == selected_city
    ]

    if selected_category != "All":
        merged = merged[
        merged["Category"] == selected_category
    ]
        
    # ==========================================
    # Show Active Filters
    # ==========================================

    st.info(f"""
    📍 City : {selected_city}

    📦 Category : {selected_category}

    🏢 Warehouse : {selected_warehouse}
    """)

    st.markdown("""

    <div style='
    padding:30px;
    border-radius:18px;
    background:linear-gradient(90deg,#2563eb,#06b6d4);
    color:white;
    '>

    <h1>🏢 AI Enterprise Intelligence Platform</h1>

    <p>Executive Decision Dashboard powered by Artificial Intelligence</p>

    </div>

    """,unsafe_allow_html=True)

    
    # ==========================================
    # KPI Calculations
    # ==========================================

    total_sales = merged["Sales"].sum()
    total_profit = merged["Profit"].sum()
    total_orders = len(merged)
    total_customers = customers["CustomerID"].nunique()
    total_products = products["ProductID"].nunique()

    average_order = orders["Sales"].mean()
    average_discount = orders["Discount"].mean()

    profit_margin = (total_profit / total_sales) * 100

    # ==========================================
    # KPI Cards
    # ==========================================

    row1 = st.columns(4)

    row1[0].metric("💰 Revenue", f"₹{total_sales:,.0f}")
    row1[1].metric("📈 Profit", f"₹{total_profit:,.0f}")
    row1[2].metric("📊 Profit Margin", f"{profit_margin:.2f}%")
    row1[3].metric("🛒 Orders", total_orders)

    row2 = st.columns(4)

    row2[0].metric("👥 Customers", total_customers)
    row2[1].metric("📦 Products", total_products)
    row2[2].metric("💵 Avg Order", f"₹{average_order:,.2f}")
    row2[3].metric("🏷 Avg Discount", f"{average_discount:.2f}%")

    st.markdown("---")

    # ==========================================
    # BUSINESS GOAL TRACKER
    # ==========================================

    st.markdown("---")

    st.subheader("🎯 Business Goal Tracker")

    # Targets
    REVENUE_TARGET = 1500000
    PROFIT_TARGET = 300000
    ORDER_TARGET = 500
    CUSTOMER_TARGET = 200

    goal1, goal2 = st.columns(2)

    with goal1:

        st.write("### 💰 Revenue Goal")

        revenue_progress = min(total_sales / REVENUE_TARGET, 1.0)

        st.progress(revenue_progress)

        st.metric(
            "Target",
            f"₹{REVENUE_TARGET:,.0f}"
        )

        if total_sales >= REVENUE_TARGET:
            st.success("✅ Revenue Target Achieved")
        else:
            st.warning(
             f"₹{REVENUE_TARGET-total_sales:,.0f} Remaining"
            )

    with goal2:

        st.write("### 📈 Profit Goal")

        profit_progress = min(total_profit / PROFIT_TARGET, 1.0)

        st.progress(profit_progress)

        st.metric(
            "Target",
            f"₹{PROFIT_TARGET:,.0f}"
        )

        if total_profit >= PROFIT_TARGET:
            st.success("✅ Profit Target Achieved")
        else:
            st.warning(
                f"₹{PROFIT_TARGET-total_profit:,.0f} Remaining"
            )

    st.markdown("---")

    goal3, goal4 = st.columns(2)

    with goal3:

        st.write("### 📦 Orders Goal")

        order_progress = min(total_orders / ORDER_TARGET, 1.0)

        st.progress(order_progress)

        st.metric(
            "Target",
            ORDER_TARGET
        )

        if total_orders >= ORDER_TARGET:
            st.success("✅ Order Target Achieved")
        else:
            st.warning(
                f"{ORDER_TARGET-total_orders} Orders Remaining"
            )

    with goal4:

        st.write("### 👥 Customer Goal")

        customer_progress = min(total_customers / CUSTOMER_TARGET, 1.0)

        st.progress(customer_progress)

        st.metric(
        "Target",
        CUSTOMER_TARGET
        )

        if total_customers >= CUSTOMER_TARGET:
            st.success("✅ Customer Target Achieved")
        else:
            st.warning(
                f"{CUSTOMER_TARGET-total_customers} Customers Remaining"
            )

    st.markdown("---")


    # ==========================================
    # EXECUTIVE KPI SCORE
    # ==========================================

    st.subheader("🏆 Executive KPI Score")

    score = 0

    if total_sales >= REVENUE_TARGET:
        score += 25

    if total_profit >= PROFIT_TARGET:
        score += 25

    if total_orders >= ORDER_TARGET:
        score += 25

    if total_customers >= CUSTOMER_TARGET:
        score += 25

    st.progress(score / 100)

    st.metric(
        "Business Achievement Score",
        f"{score}/100"
    )

    if score == 100:

        st.success("🏆 All Business Goals Achieved")

    elif score >= 75:

        st.info("📈 Business Performing Very Well")

    elif score >= 50:

        st.warning("⚠ Business Needs Improvement")

    else:

        st.error("🚨 Immediate Business Action Required")


    # ==========================================
    # SMART ALERT CENTER
    # ==========================================

    st.markdown("---")

    st.subheader("🚨 Smart Alert Center")

    alerts = []

    # Profit Margin
    if profit_margin < 15:
        alerts.append("🔴 Profit Margin is below 15%")

    # Revenue
    TARGET = 1500000

    if total_sales < TARGET:
        alerts.append("🟡 Revenue target not achieved")

    # Inventory
    low_stock = inventory[
        inventory["Stock"] <= inventory["ReorderLevel"]
    ]

    if not low_stock.empty:
        alerts.append(
            f"📦 {len(low_stock)} products need restocking"
        )

    # Discount
    if average_discount > 20:
        alerts.append(
            "🏷 Average discount is very high"
        )

    # Customer
    if total_customers < 100:
        alerts.append(
            "👥 Customer count is below expectation"
        )

    # Negative Profit Products
    negative = merged[
        merged["Profit"] < 0
    ]

    if not negative.empty:
        alerts.append(
        f"📉 {len(negative)} products are generating losses"
    )

    # Display Alerts

    st.metric(
        "Total Active Alerts",
        len(alerts)
    )

    if len(alerts) == 0:

        st.success(
            "✅ No Critical Business Alerts"
        )

    else:

        for alert in alerts:

            st.warning(alert)

    # ==========================================
    # Business Health
    # ==========================================

    st.subheader("🏢 Business Health")

    if profit_margin > 25:
        st.success("Excellent Business Performance.")
    elif profit_margin > 15:
        st.info("Business Performance is Stable.")
    else:
        st.warning("Profit Margin is Low. Review Pricing Strategy.")

    st.markdown("---")

    # ==========================================
    # Enterprise KPI Alerts
    # ==========================================

    st.subheader("🚨 Enterprise Alerts")

    if profit_margin >= 25:
        st.success("🟢 Profit Margin is Excellent.")
    elif profit_margin >= 15:
        st.warning("🟡 Profit Margin is Average.")
    else:
        st.error("🔴 Profit Margin is Low.")

    if total_sales >= 1000000:
        st.success("🟢 Revenue Target Achieved.")
    else:
        st.warning("🟡 Revenue Below Target.")

    if total_orders >= 500:
        st.success("🟢 Order Volume is Healthy.")
    else:
        st.error("🔴 Order Volume is Low.")

    if average_discount > 20:
        st.warning("🟡 High Discount Rate Detected.")
    else:
        st.success("🟢 Discount Strategy is Healthy.")

    st.markdown("---")

    # ==========================================
    # Inventory Alerts
    # ==========================================

    st.subheader("📦 Inventory Alerts")

    low_stock = inventory[
        inventory["Stock"] <= inventory["ReorderLevel"]
    ]

    if low_stock.empty:
        st.success("✅ No products require restocking.")
    else:
        st.error(f"⚠️ {len(low_stock)} products need immediate restocking.")
        st.dataframe(low_stock, use_container_width=True)

    st.markdown("---")

    st.markdown("---")

    st.subheader("🏆 Best Business Performer")

    best_product = (

        merged

        .groupby("ProductName")["Sales"]

        .sum()

        .idxmax()

    )

    best_sales = (

        merged

        .groupby("ProductName")["Sales"]

        .sum()

        .max()

    )

    st.success(f"""

    🏆 Best Product

    {best_product}

    Revenue

    ₹{best_sales:,.0f}

    """)


    st.markdown("---")

    city_sales = (

    merged

    .groupby("City")["Sales"]

    .sum()

    )

    top_city = city_sales.idxmax()

    top_city_sales = city_sales.max()

    st.info(f"""

    📍 Highest Revenue City

    {top_city}

    Revenue

    ₹{top_city_sales:,.0f}

    """)

    # ==========================================
    # Business Health Score
    # ==========================================

    score = 100

    if profit_margin < 20:
        score -= 20

    if average_discount > 20:
        score -= 10

    if len(low_stock) > 5:
        score -= 15

    score = max(score, 0)

    st.subheader("🏆 Business Health Score")

    st.progress(score / 100)

    st.metric("Business Score", f"{score}/100")

    st.markdown("---")

    # ==========================================
    # Executive Summary
    # ==========================================

    st.subheader("📋 Executive Summary")

    st.write(f"""
    **Total Revenue:** ₹{total_sales:,.0f}

    **Total Profit:** ₹{total_profit:,.0f}

    **Profit Margin:** {profit_margin:.2f}%

    **Total Customers:** {total_customers}

    **Products:** {total_products}

    **Average Order Value:** ₹{average_order:,.2f}

    **Average Discount:** {average_discount:.2f}%
    """)

    st.markdown("---")

    # ==========================================
    # Executive Analytics
    # ==========================================

    st.subheader("📈 Executive Analytics")

    orders["OrderDate"] = pd.to_datetime(orders["OrderDate"])

    monthly = (
    orders
    .groupby(pd.Grouper(key="OrderDate", freq="M"))
    .agg(
        Sales=("Sales","sum"),
        Profit=("Profit","sum"),
        Orders=("Sales","count")
    )
    .reset_index()
    )

    monthly["Revenue Growth %"] = (
    monthly["Sales"].pct_change() * 100
    )

    monthly["Profit Growth %"] = (
    monthly["Profit"].pct_change() * 100
    )

    st.dataframe(
    monthly,
    use_container_width=True
    )

    st.markdown("---")
    
  

    # =====================================================
    # Revenue Growth
    # =====================================================

    fig_growth = px.line(
    monthly,
    x="OrderDate",
    y="Revenue Growth %",
    markers=True,
    title="Monthly Revenue Growth (%)"
    )

    st.plotly_chart(
    fig_growth,
    use_container_width=True
    )

    # =====================================================
    # Profit Growth
    # =====================================================

    fig_profit = px.line(
    monthly,
    x="OrderDate",
    y="Profit Growth %",
    markers=True,
    title="Monthly Profit Growth (%)"
    )

    st.plotly_chart(
    fig_profit,
    use_container_width=True
    )

    st.markdown("---")

    # =====================================================
    # Revenue Target
    # =====================================================

    st.subheader("🎯 Revenue Target")

    TARGET = 1500000

    progress = min(total_sales / TARGET, 1)

    st.progress(progress)

    st.metric(
    "Target Achievement",
    f"{progress*100:.2f}%"
    )

    st.markdown("---")

    # =====================================================
    # Best & Worst Month
    # =====================================================

    best_month = monthly.loc[
    monthly["Sales"].idxmax()
    ]

    worst_month = monthly.loc[
    monthly["Sales"].idxmin()
    ]

    c1, c2 = st.columns(2)

    with c1:

        st.success(
        f"""
    🏆 Best Month

    {best_month['OrderDate'].strftime('%B %Y')}

    Revenue

    ₹{best_month['Sales']:,.0f}

    Profit

    ₹{best_month['Profit']:,.0f}
    """
    )

    with c2:

        st.error(
        f"""
    📉 Lowest Month

    {worst_month['OrderDate'].strftime('%B %Y')}

    Revenue

    ₹{worst_month['Sales']:,.0f}

    Profit

    ₹{worst_month['Profit']:,.0f}
    """
    )

    st.markdown("---")

    # =====================================================
    # Performance Indicator
    # =====================================================

    st.subheader("🔥 Business Performance")

    if profit_margin >= 25:

     st.success("🟢 Excellent Business Growth")

    elif profit_margin >= 15:

        st.info("🟡 Stable Business Growth")

    else:

        st.error("🔴 Business Needs Attention")

    if total_sales >= TARGET:

     st.success("🎯 Revenue Target Achieved")

    else:

        remaining = TARGET - total_sales

        st.warning(
        f"Need ₹{remaining:,.0f} more to reach target."
        )

        st.markdown("---")

    # =====================================================
    # Executive Insights
    # =====================================================

    st.subheader("📋 Executive Insights")

    highest = monthly["Sales"].max()

    lowest = monthly["Sales"].min()

    average = monthly["Sales"].mean()

    growth = monthly["Revenue Growth %"].iloc[-1]

    st.info(
    f"""
    ### Executive Summary

    • Average Monthly Revenue : ₹{average:,.0f}

    • Highest Monthly Revenue : ₹{highest:,.0f}

    • Lowest Monthly Revenue : ₹{lowest:,.0f}

    • Latest Revenue Growth : {growth:.2f}%

    ### Recommendations

    ✔ Increase inventory for top-selling products.

    ✔ Focus marketing on high-performing cities.

    ✔ Improve sales in low-performing months.

    ✔ Continue monitoring profit margin and discount strategy.

    ✔ Use AI recommendations for strategic decision-making.
    """
    )

    st.markdown("---")

    # =====================================================
    # Revenue vs Profit Comparison
    # =====================================================

    fig_compare = px.bar(
    monthly,
    x="OrderDate",
    y=["Sales", "Profit"],
    barmode="group",
    title="Revenue vs Profit Comparison"
    )

    st.plotly_chart(
    fig_compare,
    use_container_width=True
    )

    st.markdown("---")

    # =====================================================
    # Monthly Orders
    # =====================================================

    fig_orders = px.area(
    monthly,
    x="OrderDate",
    y="Orders",
    title="Monthly Orders"
    )

    st.plotly_chart(
    fig_orders,
    use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # Top Customers
    # ==========================================

    st.subheader("🏆 Top Customers")

    top_customers = (

    merged

    .groupby("CustomerName")["Sales"]

    .sum()

    .reset_index()

    .sort_values(

        "Sales",

        ascending=False

    )

    .head(10)

    )

    fig_customer = px.bar(

    top_customers,

    x="CustomerName",

    y="Sales",

    color="Sales",

    title="Top 10 Customers by Sales"

    )

    st.plotly_chart(

    fig_customer,

    use_container_width=True

    )

    st.markdown("---")
    st.markdown("---")
    # ==========================================
    # Sales by City
    # ==========================================

    st.subheader("📍 Sales by City")

    city_sales = (

    merged

    .groupby("City")["Sales"]

    .sum()

    .reset_index()

    .sort_values(

        "Sales",

        ascending=False

    )

    )

    fig_city = px.bar(

    city_sales,

    x="City",

    y="Sales",

    color="Sales",

    title="Sales by City"

    )

    st.plotly_chart(

    fig_city,

    use_container_width=True

    )
    st.markdown("---")


    # ==========================================
    # AI Executive Recommendation
    # ==========================================

    st.subheader("🤖 AI Executive Recommendation")

    try:

        recommendation = dashboard_recommendation(
            total_sales,
            total_profit,
            profit_margin,
            total_orders,
            total_customers
        )

        st.info(recommendation)

    except Exception as e:

        st.error(f"AI Error: {e}")

    st.markdown("---")

    
    # ==========================================
    # Monthly Sales Trend
    # ==========================================

    st.subheader("📅 Date Filter")

    min_date = orders["OrderDate"].min()
    max_date = orders["OrderDate"].max()

    start_date, end_date = st.date_input(
        "Select Date Range",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date()
    )

    filtered_orders = orders[
        (orders["OrderDate"].dt.date >= start_date) &
        (orders["OrderDate"].dt.date <= end_date)
    ]


    orders["OrderDate"] = pd.to_datetime(orders["OrderDate"])
    orders["Month"] = orders["OrderDate"].dt.month_name()

    month_order = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    monthly_sales = (
        orders.groupby("Month")["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Month"] = pd.Categorical(
        monthly_sales["Month"],
        categories=month_order,
        ordered=True
    )

    monthly_sales = monthly_sales.sort_values("Month")

    fig = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ==========================================
    # Top Products
    # ==========================================


    top_products = (
        merged.groupby("ProductName")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    fig2 = px.bar(
        top_products,
        x="ProductName",
        y="Sales",
        color="Sales",
        title="Top 10 Products by Sales"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ==========================================
    # Active Filters
    # ==========================================

    st.info(
    f"""
    📍 City : {selected_city}

    📦 Category : {selected_category}

    🏢 Warehouse : {selected_warehouse}
    """
    )

    # ==========================================
    # Sales by Category
    # ==========================================

    category_sales = (
        merged.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        hole=0.5,
        title="Sales by Category"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # ==========================================
    # Customer Distribution
    # ==========================================

    city_count = (
        customers["City"]
        .value_counts()
        .reset_index()
    )

    city_count.columns = ["City", "Customers"]

    fig4 = px.bar(
        city_count,
        x="City",
        y="Customers",
        color="Customers",
        title="Customers by City"
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # ==========================================
    # Inventory Status
    # ==========================================

    fig5 = px.bar(
        inventory,
        x="ProductID",
        y="Stock",
        color="Warehouse",
        title="Inventory Status"
    )

    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    # ==========================================
    # Employee Performance Dashboard
    # ==========================================

    st.markdown("---")
    st.subheader("👨‍💼 Employee Performance Dashboard")

    # Employee KPIs
    emp_col1, emp_col2, emp_col3 = st.columns(3)

    emp_col1.metric(
    "👨‍💼 Total Employees",
    len(employees)
    )

    # Department Count
    if "Department" in employees.columns:

         emp_col2.metric(
        "🏢 Departments",
         employees["Department"].nunique()
         )

    # Average Salary
    salary_column = None

    for col in ["Salary", "MonthlySalary", "EmployeeSalary"]:

        if col in employees.columns:
            salary_column = col
            break

    if salary_column:

        emp_col3.metric(
        "💰 Avg Salary",
        f"₹{employees[salary_column].mean():,.0f}"
        )

    st.markdown("---")

    # ==========================================
    # Department-wise Employees
    # ==========================================

    if "Department" in employees.columns:

        st.subheader("🏢 Department-wise Employees")

        dept = (
        employees["Department"]
        .value_counts()
        .reset_index()
        )

        dept.columns = ["Department", "Employees"]

        fig_dept = px.bar(
        dept,
        x="Department",
        y="Employees",
        color="Employees",
        title="Employees by Department"
        )

        st.plotly_chart(
        fig_dept,
        use_container_width=True
        )

        st.markdown("---")

    # ==========================================
    #   Salary Distribution
    # ==========================================

    if salary_column:

        st.subheader("💰 Salary Distribution")

        fig_salary = px.histogram(
        employees,
        x=salary_column,
        nbins=20,
        title="Employee Salary Distribution"
        )

        st.plotly_chart(
        fig_salary,
        use_container_width=True
        )

        st.markdown("---")

    # ==========================================
    # Performance Analysis
    # ==========================================

    performance_column = None

    for col in [
     "Performance",
     "PerformanceScore",
     "Rating",
     "PerformanceRating"
     ]:

        if col in employees.columns:
         performance_column = col
         break
        
    if performance_column:

        st.subheader("⭐ Employee Performance")

        fig_perf = px.bar(
            employees,
            x="EmployeeName",
            y=performance_column,
            color=performance_column,
            title="Employee Performance"
        )

        st.plotly_chart(
        fig_perf,
        use_container_width=True
        )

        st.markdown("---")

    # ==========================================
    # Employee Dataset Preview
    # ==========================================

    st.subheader("📄 Employee Records")

    st.dataframe(
    employees,
    use_container_width=True
    )
    
    # ==========================================
    # AI Executive Decision Center
    # ==========================================

    st.markdown("---")

    st.subheader("🧠 AI Executive Decision Center")

    if st.button("Generate Executive Strategy"):

        with st.spinner("AI is analyzing enterprise data..."):

            try:

                report = executive_ai(
                total_sales,
                total_profit,
                profit_margin,
                total_orders,
                total_customers,
                total_products
                )

                st.success("✅ Analysis Completed")

                st.markdown(report)
                log_activity("Generated Executive Strategy")

            except Exception as e:

                st.error(f"❌ Gemini Error: {e}")

    # ==========================================
    # Recent Orders
    # ==========================================

    st.subheader("📄 Recent Orders")

    st.dataframe(
        orders.head(20),
        use_container_width=True
    )
    

# ====================================================
# FORECAST
# ====================================================

elif page == "📈 Forecast":

    st.title("📈 Sales Forecast")

    try:

        forecast = pd.read_csv(

            "reports/sales_forecast.csv"

        )

        fig = px.line(

            forecast,

            x="ds",

            y="yhat",

            title="Predicted Sales"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    except:

        st.warning(

            "Forecast not generated yet."

        )

# ====================================================
# CUSTOMERS
# ====================================================

elif page == "👥 Customers":

    st.title("👥 Customer Analytics")

    city = st.selectbox(

        "Select City",

        sorted(customers["City"].unique())

    )

    filtered = customers[

        customers["City"] == city

    ]

    st.metric(

        "Customers",

        len(filtered)

    )

    st.dataframe(

        filtered,

        use_container_width=True

    )

# ====================================================
# INVENTORY
# ====================================================

elif page == "📦 Inventory":

    st.title("📦 Inventory")

    st.dataframe(

        inventory,

        use_container_width=True

    )

    fig = px.bar(

        inventory,

        x="ProductID",

        y="Stock",

        color="Warehouse",

        title="Inventory"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ====================================================
# AI
# ====================================================

elif page == "🤖 AI Assistant":

    from enterprise.pages.AI_Assistant import ai_page

    log_activity("Opened AI Business Assistant")

    ai_page()

# ====================================================
# REPORTS
# ====================================================

elif page == "📄 Reports":

    if st.session_state.role != "Admin":

        st.error("❌ Access Denied")
        st.stop()

    st.title("📄 Business Reports")

    # ==========================================
    # KPI Calculations
    # ==========================================

    total_sales = orders["Sales"].sum()
    total_profit = orders["Profit"].sum()
    total_orders = len(orders)
    total_customers = customers["CustomerID"].nunique()
    total_products = products["ProductID"].nunique()
    profit_margin = (total_profit / total_sales) * 100

    st.markdown("---")

    # ==========================================
    # Select Report
    # ==========================================

    report = st.selectbox(
        "Select Report",
        [
            "Orders",
            "Customers",
            "Products",
            "Inventory",
            "Marketing",
            "Employees"
        ]
    )

    # ==========================================
    # Select Dataset
    # ==========================================

    if report == "Orders":
        df = orders

    elif report == "Customers":
        df = customers

    elif report == "Products":
        df = products

    elif report == "Inventory":
        df = inventory

    elif report == "Marketing":
        df = marketing

    else:
        df = employees

    # ==========================================
    # Preview
    # ==========================================

    st.subheader("📄 Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    # ==========================================
    # CSV Download
    # ==========================================

    csv = df.to_csv(index=False)

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name=f"{report}.csv",
        mime="text/csv"
    )
    log_activity("Downloaded CSV Report")

    # ==========================================
    # Excel Download
    # ==========================================

    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name=report
        )

    st.download_button(
        label="⬇ Download Excel",
        data=buffer.getvalue(),
        file_name=f"{report}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    log_activity("Downloaded Excel Report")

    # ==========================================
    # PDF Download
    # ==========================================

    pdf_file = "reports/Executive_Report.pdf"

    generate_pdf(
        pdf_file,
        total_sales,
        total_profit,
        profit_margin,
        total_orders,
        total_customers,
        total_products
    )

    with open(pdf_file, "rb") as f:

        st.download_button(
            label="📄 Download PDF Report",
            data=f,
            file_name="Executive_Report.pdf",
            mime="application/pdf"
        )
        log_activity("Downloaded PDF Report")

    # ==========================================
    # Report Summary
    # ==========================================

    st.markdown("---")

    st.subheader("📊 Report Summary")

    st.write(f"Rows : {df.shape[0]}")
    st.write(f"Columns : {df.shape[1]}")

    st.markdown("---")


# ====================================================
# AUDIT LOG
# ====================================================


elif page == "📜 Audit Log":

    if st.session_state.role != "Admin":

        st.error("❌ Access Denied")

        st.stop()

    st.title("📜 Activity Log")

    st.markdown("---")

    try:

        logs = pd.read_csv(
            "logs/activity_log.csv"
        )

        st.dataframe(
            logs,
            use_container_width=True
        )

        st.metric(
            "Total Activities",
            len(logs)
        )

    except:

        st.info("No activity found.")
    st.markdown("---")

    

# ==========================================
#  Settings
# ==========================================

elif page == "⚙ Settings":

    if st.session_state.role != "Admin":

        st.error("❌ Access Denied")
        st.stop()

    st.title("⚙ Settings")

    st.markdown("---")

    st.subheader("🎨 Application Settings")

    dark_mode = st.toggle(
        "🌙 Dark Mode",
        value=True
    )

    notifications = st.checkbox(
        "🔔 Enable Notifications",
        value=True
    )

    auto_refresh = st.checkbox(
        "🔄 Auto Refresh Dashboard"
    )

    refresh_time = st.slider(
        "Refresh Interval",
        10,
        300,
        60
    )

    st.markdown("---")

    st.subheader("👤 Profile")

    st.write(f"User : {st.session_state.user}")

    st.write(f"Role : {st.session_state.role}")

    st.markdown("---")

    if st.button("💾 Save Settings"):

        log_activity("Updated Settings")

        st.success("Settings Saved Successfully!")


st.markdown("""

<center>

AI Enterprise Intelligence Platform

Version 2.0

Built with ❤️ using Python • Streamlit • Gemini AI • Plotly 

By Sharau Jagtap

</center>

""",unsafe_allow_html=True)