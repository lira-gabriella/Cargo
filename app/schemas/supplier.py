from typing import Optional

from pydantic import BaseModel, ConfigDict


class SupplierBase(BaseModel):
    supplier_name: str
    country: str


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    supplier_name: Optional[str] = None
    country: Optional[str] = None


class SupplierRead(SupplierBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
