import pandas as pd

from app.data.loader import load_products, load_sales


def get_sales_summary(days: int = 30):
    sales = load_sales()
    products = load_products()

    max_date = sales["date"].max()
    start_date = max_date - pd.Timedelta(days=days - 1)

    recent_sales = sales[sales["date"] >= start_date]

    summary = (
        recent_sales
        .groupby("sku", as_index=False)
        .agg(
            units_sold=("units_sold", "sum"),
            revenue=("revenue", "sum"),
        )
    )

    summary["avg_daily_sales"] = summary["units_sold"] / days

    result = summary.merge(
        products,
        on="sku",
        how="left",
    )

    result = result[
        [
            "sku",
            "product_name",
            "category",
            "units_sold",
            "avg_daily_sales",
            "revenue",
        ]
    ]

    result = result.sort_values("units_sold", ascending=False)

    return {
        "period_days": days,
        "from_date": str(start_date.date()),
        "to_date": str(max_date.date()),
        "items": result.to_dict(orient="records"),
    }