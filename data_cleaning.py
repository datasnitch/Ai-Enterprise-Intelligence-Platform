import pandas as pd

# Load datasets
customers = pd.read_csv("data/raw/customers.csv")
products = pd.read_csv("data/raw/products.csv")
orders = pd.read_csv("data/raw/orders.csv")
marketing = pd.read_csv("data/raw/marketing.csv")
inventory = pd.read_csv("data/raw/inventory.csv")
employees = pd.read_csv("data/raw/employees.csv")

print("All datasets loaded successfully!")

# Remove duplicates
customers = customers.drop_duplicates()
products = products.drop_duplicates()
orders = orders.drop_duplicates()
marketing = marketing.drop_duplicates()
inventory = inventory.drop_duplicates()
employees = employees.drop_duplicates()

# Fill missing values
customers["Age"] = customers["Age"].fillna(customers["Age"].mean())
customers["City"] = customers["City"].fillna("Unknown")

# Convert dates
customers["JoinDate"] = pd.to_datetime(customers["JoinDate"])
orders["OrderDate"] = pd.to_datetime(orders["OrderDate"])

# Feature Engineering
orders["Month"] = orders["OrderDate"].dt.month
orders["Year"] = orders["OrderDate"].dt.year
orders["Quarter"] = orders["OrderDate"].dt.quarter
orders["ProfitMargin"] = (orders["Profit"] / orders["Sales"]) * 100
orders["AverageOrderValue"] = orders["Sales"] / orders["Quantity"]

# Save cleaned datasets
customers.to_csv("data/cleaned/customers_clean.csv", index=False)
products.to_csv("data/cleaned/products_clean.csv", index=False)
orders.to_csv("data/cleaned/orders_clean.csv", index=False)
marketing.to_csv("data/cleaned/marketing_clean.csv", index=False)
inventory.to_csv("data/cleaned/inventory_clean.csv", index=False)
employees.to_csv("data/cleaned/employees_clean.csv", index=False)

print("Cleaning Completed!")
print("Clean files saved successfully!")