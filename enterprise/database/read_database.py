import pandas as pd

from mysql_connector import connect

conn = connect()

orders = pd.read_sql(
    "SELECT * FROM Orders",
    conn
)

customers = pd.read_sql(
    "SELECT * FROM Customers",
    conn
)

products = pd.read_sql(
    "SELECT * FROM Products",
    conn
)

inventory = pd.read_sql(
    "SELECT * FROM Inventory",
    conn
)

marketing = pd.read_sql(
    "SELECT * FROM Marketing",
    conn
)

employees = pd.read_sql(
    "SELECT * FROM Employees",
    conn
)

print(orders.head())

conn.close()