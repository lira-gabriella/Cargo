from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.receipt import ReceiptRead
from app.services import receipt_service

router = APIRouter(
    prefix="/receipts", tags=["receipts"], dependencies=[Depends(get_current_user)]
)


@router.get("/{receipt_id}", response_model=ReceiptRead)
def get_receipt(receipt_id: int, db: Session = Depends(get_db)):
    return receipt_service.get_receipt(db, receipt_id)


@router.get("/by-sale/{sale_id}", response_model=ReceiptRead)
def get_receipt_by_sale(sale_id: int, db: Session = Depends(get_db)):
    return receipt_service.get_receipt_by_sale(db, sale_id)
