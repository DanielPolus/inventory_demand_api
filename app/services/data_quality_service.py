import pandas as pd

from app.data.loader import (
    load_inventory,
    load_products,
    load_promotions,
    load_purchase_orders,
    load_sales,
    load_suppliers,
)


def get_missing_values(df: pd.DataFrame) -> dict:
    missing = df.isna().sum()
    return {
        column: int(count)
        for column, count in missing.items()
        if count > 0
    }


def get_data_quality_report():
    products = load_products()
    sales = load_sales()
    inventory = load_inventory()
    suppliers = load_suppliers()
    promotions = load_promotions()
    purchase_orders = load_purchase_orders()

    report = {
        "status": "ok",
        "tables": {
            "products": {
                "rows": len(products),
                "columns": list(products.columns),
                "missing_values": get_missing_values(products),
                "duplicate_rows": int(products.duplicated().sum()),
            },
            "sales_daily": {
                "rows": len(sales),
                "columns": list(sales.columns),
                "missing_values": get_missing_values(sales),
                "duplicate_rows": int(sales.duplicated().sum()),
                "date_from": str(sales["date"].min().date()),
                "date_to": str(sales["date"].max().date()),
                "unique_skus": int(sales["sku"].nunique()),
                "unique_warehouses": int(sales["warehouse_id"].nunique()),
            },
            "current_inventory": {
                "rows": len(inventory),
                "columns": list(inventory.columns),
                "missing_values": get_missing_values(inventory),
                "duplicate_rows": int(inventory.duplicated().sum()),
                "unique_skus": int(inventory["sku"].nunique()),
                "unique_warehouses": int(inventory["warehouse_id"].nunique()),
            },
            "suppliers": {
                "rows": len(suppliers),
                "columns": list(suppliers.columns),
                "missing_values": get_missing_values(suppliers),
                "duplicate_rows": int(suppliers.duplicated().sum()),
            },
            "promotions": {
                "rows": len(promotions),
                "columns": list(promotions.columns),
                "missing_values": get_missing_values(promotions),
                "duplicate_rows": int(promotions.duplicated().sum()),
            },
            "purchase_orders": {
                "rows": len(purchase_orders),
                "columns": list(purchase_orders.columns),
                "missing_values": get_missing_values(purchase_orders),
                "duplicate_rows": int(purchase_orders.duplicated().sum()),
            },
        },
        "summary": {
            "products_count": int(products["sku"].nunique()),
            "categories_count": int(products["category"].nunique()),
            "warehouses_count": int(inventory["warehouse_id"].nunique()),
            "sales_rows": len(sales),
            "sales_period_days": int(
                (sales["date"].max() - sales["date"].min()).days + 1
            ),
        },
    }

    return report