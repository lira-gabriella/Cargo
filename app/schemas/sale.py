from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator

from app.models.sale import LogType
from app.schemas.sale_item import SaleItemCreate, SaleItemRead


class SaleCreate(BaseModel):
    customer_id: int
    log_type: LogType
    items: list[SaleItemCreate]

    @field_validator("items")
    @classmethod
    def items_not_empty(cls, v):
        if not v:
            raise ValueError("A sale must contain at least one item")
        return v


class SaleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    user_id: int
    log_type: LogType
    sale_date: datetime
    total_amount: Decimal
    items: list[SaleItemRead] = []
