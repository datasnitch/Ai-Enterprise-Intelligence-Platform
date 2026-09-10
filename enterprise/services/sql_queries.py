import pandas as pd

from enterprise.database.mysql_connector import connect

# ------------------------------------------
# Top Products
# ------------------------------------------

def get_top_products():

    conn = connect()

    query = """
    SELECT
        p.ProductName,
        SUM(o.Sales) AS TotalSales
    FROM Orders o
    JOIN Products p
    ON o.ProductID = p.ProductID
    GROUP BY p.ProductName
    ORDER BY TotalSales DESC
    LIMIT 10;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# ------------------------------------------
# Top Customers
# ------------------------------------------

def get_top_customers():

    conn = connect()

    query = """
    SELECT
        c.CustomerName,
        SUM(o.Sales) AS Revenue
    FROM Orders o
    JOIN Customers c
    ON o.CustomerID=c.CustomerID
    GROUP BY c.CustomerName
    ORDER BY Revenue DESC
    LIMIT 10;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# ------------------------------------------
# Monthly Sales
# ------------------------------------------

def get_monthly_sales():

    conn = connect()

    query = """
    SELECT

    Month,

    SUM(Sales) AS Sales

    FROM Orders

    GROUP BY Month

    ORDER BY Month;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# ------------------------------------------
# Profit By Category
# ------------------------------------------

def get_profit_by_category():

    conn = connect()

    query = """
    SELECT

    p.Category,

    SUM(o.Profit) AS Profit

    FROM Orders o

    JOIN Products p

    ON o.ProductID=p.ProductID

    GROUP BY p.Category;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# ------------------------------------------
# City Wise Customers
# ------------------------------------------

def get_city_customers():

    conn = connect()

    query = """
    SELECT

    City,

    COUNT(*) AS Customers

    FROM Customers

    GROUP BY City

    ORDER BY Customers DESC;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# ------------------------------------------
# Low Stock Products
# ------------------------------------------

def get_low_stock():

    conn = connect()

    query = """
    SELECT

    ProductID,

    Stock,

    ReorderLevel

    FROM Inventory

    WHERE Stock<ReorderLevel;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df