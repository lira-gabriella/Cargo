from pydantic import BaseModel, ConfigDict


class ReceiptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sale_id: int
    gate_pass_code: str
