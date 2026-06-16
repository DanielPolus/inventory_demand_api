import math

import numpy as np
import pandas as pd

from typing import Optional

from app.data.loader import (
    load_inventory,
    load_products,
    load_purchase_orders,
    load_sales,
    load_suppliers,
)


def clean_records(df: pd.DataFrame) -> list[dict]:
    """
    Converts DataFrame to JSON-safe records.
    Replaces NaN / inf values with None.
    """
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.astype(object).where(pd.notnull(df), None)
    return df.to_dict(orient="records")


def round_up_to_pack_size(quantity: int, pack_size: int) -> int:
    if quantity <= 0:
        return 0

    if pack_size <= 0:
        return quantity

    return int(math.ceil(quantity / pack_size) * pack_size)


def get_replenishment_recommendations(
    target_days: int = 30,
    category: Optional[str] = None,
    warehouse_id: Optional[str] = None,
    priority: Optional[str] = None,
    limit: Optional[int] = None,
):
    sales = load_sales()
    products = load_products()
    inventory = load_inventory()
    suppliers = load_suppliers()
    purchase_orders = load_purchase_orders()

    max_date = sales["date"].max()
    start_date = max_date - pd.Timedelta(days=29)

    recent_sales = sales[sales["date"] >= start_date]

    demand = recent_sales.groupby(["sku", "warehouse_id"], as_index=False).agg(
        units_sold_30d=("units_sold", "sum")
    )

    demand["avg_daily_sales"] = demand["units_sold_30d"] / 30

    open_orders = purchase_orders[
        purchase_orders["status"].isin(["ordered", "in_transit"])
    ]

    incoming = open_orders.groupby(["sku", "warehouse_id"], as_index=False).agg(
        incoming_stock=("ordered_units", "sum")
    )

    result = (
        inventory.merge(products, on="sku", how="left", suffixes=("", "_product"))
        .merge(demand, on=["sku", "warehouse_id"], how="left")
        .merge(incoming, on=["sku", "warehouse_id"], how="left")
        .merge(
            suppliers[["supplier_id", "supplier_name"]],
            on="supplier_id",
            how="left",
        )
    )

    result["avg_daily_sales"] = result["avg_daily_sales"].fillna(0)
    result["units_sold_30d"] = result["units_sold_30d"].fillna(0)
    result["incoming_stock"] = result["incoming_stock"].fillna(0)

    result["current_stock"] = result["available_units"]

    result["forecast_target_period"] = result["avg_daily_sales"] * target_days

    result["forecast_during_lead_time"] = (
        result["avg_daily_sales"] * result["lead_time_days"]
    )

    result["safety_stock"] = result["avg_daily_sales"] * 7

    result["raw_recommended_order_qty"] = (
        result["forecast_target_period"]
        + result["forecast_during_lead_time"]
        + result["safety_stock"]
        - result["current_stock"]
        - result["incoming_stock"]
    )

    result["raw_recommended_order_qty"] = (
        result["raw_recommended_order_qty"].clip(lower=0).round().astype(int)
    )

    result["recommended_order_qty"] = result.apply(
        lambda row: round_up_to_pack_size(
            row["raw_recommended_order_qty"],
            row["order_pack_size"],
        ),
        axis=1,
    )

    def define_priority(row):
        if row["recommended_order_qty"] == 0:
            return "NO_ORDER_NEEDED"

        if row["current_stock"] <= row["forecast_during_lead_time"]:
            return "URGENT"

        if row["recommended_order_qty"] > row["avg_daily_sales"] * 14:
            return "HIGH"

        return "NORMAL"

    result["priority"] = result.apply(define_priority, axis=1)

    if category:
        result = result[result["category"].str.lower() == category.lower()]

    if warehouse_id:
        result = result[result["warehouse_id"].str.lower() == warehouse_id.lower()]

    if priority:
        result = result[result["priority"].str.upper() == priority.upper()]

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
            "incoming_stock",
            "avg_daily_sales",
            "units_sold_30d",
            "forecast_target_period",
            "forecast_during_lead_time",
            "safety_stock",
            "raw_recommended_order_qty",
            "recommended_order_qty",
            "order_pack_size",
            "priority",
            "supplier_id",
            "supplier_name",
            "lead_time_days",
        ]
    ]

    priority_order = {
        "URGENT": 1,
        "HIGH": 2,
        "NORMAL": 3,
        "NO_ORDER_NEEDED": 4,
    }

    result["priority_sort"] = result["priority"].map(priority_order)

    result = result.sort_values(
        by=["priority_sort", "recommended_order_qty"],
        ascending=[True, False],
    )

    result = result.drop(columns=["priority_sort"])

    if limit:
        result = result.head(limit)

    return {
        "target_days": target_days,
        "method": "avg_demand_plus_lead_time_safety_stock_and_pack_size",
        "filters": {
            "category": category,
            "warehouse_id": warehouse_id,
            "priority": priority,
            "limit": limit,
        },
        "items_count": len(result),
        "items": clean_records(result),
    }


def get_product_replenishment_recommendation(
    sku: str,
    target_days: int = 30,
):
    recommendations = get_replenishment_recommendations(target_days=target_days)

    items = [item for item in recommendations["items"] if item["sku"] == sku]

    if not items:
        return None

    return {
        "sku": sku,
        "target_days": target_days,
        "items_count": len(items),
        "items": items,
    }
