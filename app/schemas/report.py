from decimal import Decimal

from pydantic import BaseModel

from schemas.sale import SaleRead


class WarehouseStatusReport(BaseModel):
    total_sales: int
    total_revenue: Decimal
    pending_payments: int
    recent_sales: list[SaleRead]
