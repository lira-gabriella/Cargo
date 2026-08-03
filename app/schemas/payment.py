from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PaymentCreate(BaseModel):
    sale_id: int
    method: str
    amount_paid: Decimal


class PaymentRead(PaymentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
