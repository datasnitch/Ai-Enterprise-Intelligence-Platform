import pandas as pd


def load_all_data():

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