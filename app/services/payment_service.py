import secrets

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.payment_repo import payment_repository
from app.repositories.receipt_repo import receipt_repository
from app.repositories.sale_repo import sale_repository
from app.schemas.payment import PaymentCreate


def get_payment(db: Session, payment_id: int):
    payment = payment_repository.get(db, payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment


def record_payment(db: Session, data: PaymentCreate):
    sale = sale_repository.get(db, data.sale_id)
    if not sale:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sale not found")
    if sale.payment is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This sale has already been paid"
        )
    if data.amount_paid < sale.total_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount paid is less than the total amount due",
        )

    payment = payment_repository.create(db, data.model_dump())

    gate_pass_code = secrets.token_hex(8).upper()
    receipt_repository.create(db, {"sale_id": sale.id, "gate_pass_code": gate_pass_code})

    return payment
