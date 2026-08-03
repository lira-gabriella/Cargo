from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    service_name: str
    category_id: int
    supplier_id: int
    price: Decimal


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    service_name: Optional[str] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    price: Optional[Decimal] = None


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
