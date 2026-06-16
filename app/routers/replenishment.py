from fastapi import APIRouter, HTTPException, Query

from typing import Optional

from app.services.replenishment_service import (
    get_product_replenishment_recommendation,
    get_replenishment_recommendations,
)


router = APIRouter(prefix="/replenishment", tags=["Replenishment"])


@router.get("/recommendations")
def read_replenishment_recommendations(
    target_days: int = Query(default=30, ge=1, le=90),
    category: Optional[str] = Query(default=None),
    warehouse_id: Optional[str] = Query(default=None),
    priority: Optional[str] = Query(
        default=None,
        description="Available values: URGENT, HIGH, NORMAL, NO_ORDER_NEEDED",
    ),
    limit: Optional[int] = Query(default=None, ge=1, le=500),
):
    return get_replenishment_recommendations(
        target_days=target_days,
        category=category,
        warehouse_id=warehouse_id,
        priority=priority,
        limit=limit,
    )


@router.get("/recommendations/{sku}")
def read_product_replenishment_recommendation(
    sku: str,
    target_days: int = Query(default=30, ge=1, le=90),
):
    result = get_product_replenishment_recommendation(
        sku=sku,
        target_days=target_days,
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return result