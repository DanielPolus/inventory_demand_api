from fastapi import APIRouter, HTTPException, Query

from app.services.replenishment_service import (
    get_product_replenishment_recommendation,
    get_replenishment_recommendations,
)


router = APIRouter(prefix="/replenishment", tags=["Replenishment"])


@router.get("/recommendations")
def read_replenishment_recommendations(
    target_days: int = Query(default=30, ge=1, le=90),
):
    return get_replenishment_recommendations(target_days=target_days)


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