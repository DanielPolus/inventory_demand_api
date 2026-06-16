from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.services.inventory_risk_service import (
    get_product_stockout_risk,
    get_stockout_risk,
)


router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/stockout-risk")
def read_stockout_risk(
    category: Optional[str] = Query(default=None),
    warehouse_id: Optional[str] = Query(default=None),
    risk_level: Optional[str] = Query(
        default=None,
        description="Available values: HIGH, MEDIUM, LOW, NO_DEMAND",
    ),
    limit: Optional[int] = Query(default=None, ge=1, le=500),
):
    return get_stockout_risk(
        category=category,
        warehouse_id=warehouse_id,
        risk_level=risk_level,
        limit=limit,
    )


@router.get("/stockout-risk/{sku}")
def read_product_stockout_risk(sku: str):
    result = get_product_stockout_risk(sku)

    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return result