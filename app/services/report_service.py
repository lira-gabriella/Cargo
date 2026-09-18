from decimal import Decimal

from sqlalchemy.orm import Session

from app.repositories.sale_repo import sale_repository


def get_status_report(db: Session, recent_limit: int = 10):
    sales = sale_repository.get_all(db)
    total_revenue = sum((s.total_amount for s in sales), Decimal("0"))
    pending_payments = sum(1 for s in sales if s.payment is None)
    recent_sales = sorted(sales, key=lambda s: s.sale_date, reverse=True)[:recent_limit]
    return {
        "total_sales": len(sales),
        "total_revenue": total_revenue,
        "pending_payments": pending_payments,
        "recent_sales": recent_sales,
    }
