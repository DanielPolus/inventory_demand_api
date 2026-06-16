from fastapi import APIRouter, Query

from app.services.analytics_service import get_sales_summary


router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/sales-summary")
def read_sales_summary(days: int = Query(default=30, ge=1, le=365)):
    return get_sales_summary(days=days)