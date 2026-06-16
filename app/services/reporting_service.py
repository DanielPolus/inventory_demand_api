from io import StringIO

import pandas as pd

from app.services.replenishment_service import get_replenishment_recommendations


def generate_replenishment_csv(target_days: int = 30) -> str:
    recommendations = get_replenishment_recommendations(target_days=target_days)

    items = recommendations["items"]

    df = pd.DataFrame(items)

    export_columns = [
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

    df = df[export_columns]

    output = StringIO()
    df.to_csv(output, index=False)

    return output.getvalue()