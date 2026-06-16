from fastapi import FastAPI

from app.routers import (
    analytics,
    data_quality,
    forecast,
    inventory,
    products,
    replenishment,
    reports,
)

app = FastAPI(
    title="Inventory Demand Forecasting API",
    description=(
        "Mini ERP module for demand forecasting, stockout risk analysis "
        "and replenishment recommendations."
    ),
    version="0.1.0",
)


app.include_router(products.router)
app.include_router(analytics.router)
app.include_router(forecast.router)
app.include_router(inventory.router)
app.include_router(replenishment.router)
app.include_router(reports.router)
app.include_router(data_quality.router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "inventory-demand-api",
        "version": "0.1.0",
    }
