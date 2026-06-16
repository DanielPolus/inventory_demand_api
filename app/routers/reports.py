from fastapi import APIRouter, Query
from fastapi.responses import Response

from typing import Optional

from app.services.reporting_service import generate_replenishment_csv

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/replenishment.csv")
def download_replenishment_report(
    target_days: int = Query(default=30, ge=1, le=90),
    category: Optional[str] = Query(default=None),
    warehouse_id: Optional[str] = Query(default=None),
    priority: Optional[str] = Query(
        default=None,
        description="Available values: URGENT, HIGH, NORMAL, NO_ORDER_NEEDED",
    ),
):
    csv_content = generate_replenishment_csv(
        target_days=target_days,
        category=category,
        warehouse_id=warehouse_id,
        priority=priority,
    )

    filename = f"replenishment_report_{target_days}_days.csv"

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
