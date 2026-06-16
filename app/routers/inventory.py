from fastapi import APIRouter, HTTPException

from app.services.inventory_risk_service import (
    get_product_stockout_risk,
    get_stockout_risk,
)


router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/stockout-risk")
def read_stockout_risk():
    return get_stockout_risk()


@router.get("/stockout-risk/{sku}")
def read_product_stockout_risk(sku: str):
    result = get_product_stockout_risk(sku)

    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return result