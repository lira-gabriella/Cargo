from typing import Optional

from pydantic import BaseModel, ConfigDict


class CustomerBase(BaseModel):
    company_name: str
    tin_number: str
    phone_number: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    company_name: Optional[str] = None
    tin_number: Optional[str] = None
    phone_number: Optional[str] = None


class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
