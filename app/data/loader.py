from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"


def load_products() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_DIR / "products.csv")


def load_sales() -> pd.DataFrame:
    sales = pd.read_csv(RAW_DATA_DIR / "sales_daily.csv")
    sales["date"] = pd.to_datetime(sales["date"])
    return sales


def load_inventory() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_DIR / "current_inventory.csv")


def load_suppliers() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_DIR / "suppliers.csv")


def load_promotions() -> pd.DataFrame:
    promotions = pd.read_csv(RAW_DATA_DIR / "promotions.csv")
    promotions["start_date"] = pd.to_datetime(promotions["start_date"])
    promotions["end_date"] = pd.to_datetime(promotions["end_date"])
    return promotions


def load_purchase_orders() -> pd.DataFrame:
    orders = pd.read_csv(RAW_DATA_DIR / "purchase_orders.csv")
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    orders["expected_delivery_date"] = pd.to_datetime(orders["expected_delivery_date"])
    return orders
