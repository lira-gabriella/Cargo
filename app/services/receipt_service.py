from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.receipt_repo import receipt_repository


def get_receipt(db: Session, receipt_id: int):
    receipt = receipt_repository.get(db, receipt_id)
    if not receipt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
    return receipt


def get_receipt_by_sale(db: Session, sale_id: int):
    receipt = receipt_repository.get_by_sale(db, sale_id)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No receipt for this sale yet"
        )
    return receipt
