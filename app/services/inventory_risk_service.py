import numpy as np
import pandas as pd
from typing import Optional

from app.data.loader import load_inventory, load_products, load_sales, load_suppliers


def clean_records(df: pd.DataFrame) -> list[dict]:
    """
    Converts DataFrame to JSON-safe records.
    Replaces NaN / inf values with None.
    """
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.astype(object).where(pd.notnull(df), None)
    return df.to_dict(orient="records")


def get_stockout_risk(
    category: Optional[str] = None,
    warehouse_id: Optional[str] = None,
    risk_level: Optional[str] = None,
    limit: Optional[int] = None,
):
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

    result["current_stock"] = result["available_units"]

    result["days_until_stockout"] = np.where(
        result["avg_daily_sales"] > 0,
        result["current_stock"] / result["avg_daily_sales"],
        np.nan,
    )

    def define_risk_level(row):
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

    result["risk_level"] = result.apply(define_risk_level, axis=1)

    if category:
        result = result[result["category"].str.lower() == category.lower()]

    if warehouse_id:
        result = result[result["warehouse_id"].str.lower() == warehouse_id.lower()]

    if risk_level:
        result = result[result["risk_level"].str.upper() == risk_level.upper()]

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

    if limit:
        result = result.head(limit)

    return {
        "method": "available_stock_vs_30_day_average_demand",
        "filters": {
            "category": category,
            "warehouse_id": warehouse_id,
            "risk_level": risk_level,
            "limit": limit,
        },
        "items_count": len(result),
        "items": clean_records(result),
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
        "items_count": len(items),
        "items": items,
    }