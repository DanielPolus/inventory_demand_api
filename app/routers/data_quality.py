from fastapi import APIRouter

from app.services.data_quality_service import get_data_quality_report

router = APIRouter(prefix="/data", tags=["Data Quality"])


@router.get("/quality-check")
def read_data_quality_report():
    return get_data_quality_report()
