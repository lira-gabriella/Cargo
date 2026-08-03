from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from routers.auth import get_current_user
from schemas.report import WarehouseStatusReport
from services import report_service

router = APIRouter(
    prefix="/reports", tags=["reports"], dependencies=[Depends(get_current_user)]
)


@router.get("/status", response_model=WarehouseStatusReport)
def warehouse_status(db: Session = Depends(get_db)):
    return report_service.get_status_report(db)
