from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.payment import PaymentCreate, PaymentRead
from app.services import payment_service

router = APIRouter(
    prefix="/payments", tags=["payments"], dependencies=[Depends(get_current_user)]
)


@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    return payment_service.get_payment(db, payment_id)


@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def record_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    return payment_service.record_payment(db, data)
