from fastapi import APIRouter, HTTPException, Query

from app.services.forecasting_service import (
    get_demand_forecast,
    get_product_demand_forecast,
)

router = APIRouter(prefix="/forecast", tags=["Forecast"])


@router.get("")
def read_forecast(days: int = Query(default=30, ge=1, le=90)):
    return get_demand_forecast(days=days)


@router.get("/{sku}")
def read_product_forecast(
    sku: str,
    days: int = Query(default=30, ge=1, le=90),
):
    result = get_product_demand_forecast(sku=sku, days=days)

    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return result
