import numpy as np
import pandas as pd

from app.data.loader import load_inventory, load_products, load_sales, load_suppliers


def get_stockout_risk():
    sales = load_sales()
    products = load_products()
    inventory = load_inventory()
    suppliers = load_suppliers()

    max_date = sales["date"].max()
    start_date = max_date - pd.Timedelta(days=29)
    recent_sales = sales[sales["date"] >= start_date]

    demand = (
        recent_sales
        .groupby(["sku", "warehouse_id"], as_index=False)
        .agg(units_sold_30d=("units_sold", "sum"))
    )

    demand["avg_daily_sales"] = demand["units_sold_30d"] / 30

    result = (
        inventory
        .merge(products, on="sku", how="left", suffixes=("", "_product"))
        .merge(demand, on=["sku", "warehouse_id"], how="left")
        .merge(
            suppliers[["supplier_id", "supplier_name"]],
            on="supplier_id",
            how="left",
        )
    )

    result["avg_daily_sales"] = result["avg_daily_sales"].fillna(0)
    result["units_sold_30d"] = result["units_sold_30d"].fillna(0)

    # Для бизнеса важнее доступный остаток, а не весь физический остаток.
    result["current_stock"] = result["available_units"]

    result["days_until_stockout"] = np.where(
        result["avg_daily_sales"] > 0,
        result["current_stock"] / result["avg_daily_sales"],
        np.nan,
    )

    def risk_level(row):
        avg_daily_sales = row["avg_daily_sales"]
        days_until_stockout = row["days_until_stockout"]
        lead_time = row["lead_time_days"]

        if avg_daily_sales == 0:
            return "NO_DEMAND"

        if days_until_stockout <= lead_time:
            return "HIGH"

        if days_until_stockout <= 14:
            return "MEDIUM"

        return "LOW"

    result["risk_level"] = result.apply(risk_level, axis=1)

    result = result[
        [
            "sku",
            "product_name",
            "category",
            "warehouse_id",
            "warehouse_name",
            "current_stock",
            "on_hand_units",
            "reserved_units",
            "avg_daily_sales",
            "units_sold_30d",
            "days_until_stockout",
            "supplier_id",
            "supplier_name",
            "lead_time_days",
            "risk_level",
        ]
    ]

    risk_order = {
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
        "NO_DEMAND": 4,
    }

    result["risk_sort"] = result["risk_level"].map(risk_order)

    result = result.sort_values(
        by=["risk_sort", "days_until_stockout"],
        ascending=[True, True],
    )

    result = result.drop(columns=["risk_sort"])

    return {
        "method": "available_stock_vs_30_day_average_demand",
        "items": result.to_dict(orient="records"),
    }


def get_product_stockout_risk(sku: str):
    risks = get_stockout_risk()

    items = [
        item for item in risks["items"]
        if item["sku"] == sku
    ]

    if not items:
        return None

    return {
        "sku": sku,
        "items": items,
    }