from fastapi import APIRouter, Query
from fastapi.responses import Response

from app.services.reporting_service import generate_replenishment_csv


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/replenishment.csv")
def download_replenishment_report(
    target_days: int = Query(default=30, ge=1, le=90),
):
    csv_content = generate_replenishment_csv(target_days=target_days)

    filename = f"replenishment_report_{target_days}_days.csv"

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )