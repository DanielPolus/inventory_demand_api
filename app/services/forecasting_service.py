import pandas as pd

from app.data.loader import load_products, load_sales


def get_demand_forecast(days: int = 30):
    sales = load_sales()
    products = load_products()

    max_date = sales["date"].max()

    # Берём последние 30 дней как базу для прогноза
    start_date = max_date - pd.Timedelta(days=29)
    recent_sales = sales[sales["date"] >= start_date]

    summary = (
        recent_sales
        .groupby("sku", as_index=False)
        .agg(
            units_sold_30d=("units_sold", "sum"),
        )
    )

    summary["avg_daily_sales"] = summary["units_sold_30d"] / 30
    summary["forecast_units"] = (summary["avg_daily_sales"] * days).round().astype(int)

    result = summary.merge(products, on="sku", how="left")

    result = result[
        [
            "sku",
            "product_name",
            "category",
            "units_sold_30d",
            "avg_daily_sales",
            "forecast_units",
        ]
    ]

    result = result.sort_values("forecast_units", ascending=False)

    return {
        "forecast_days": days,
        "method": "30_day_moving_average",
        "items": result.to_dict(orient="records"),
    }


def get_product_demand_forecast(sku: str, days: int = 30):
    forecast = get_demand_forecast(days=days)

    for item in forecast["items"]:
        if item["sku"] == sku:
            return {
                "forecast_days": days,
                "method": forecast["method"],
                "item": item,
            }

    return None