from decimal import Decimal

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.sale_repo import sale_repository
from app.repositories.sale_item_repo import sale_item_repository
from app.repositories.product_repo import product_repository
from app.repositories.customer_repo import customer_repository
from app.schemas.sale import SaleCreate


def get_sale(db: Session, sale_id: int):
    sale = sale_repository.get(db, sale_id)
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return sale


def list_sales(db: Session):
    return sale_repository.get_all(db)


def create_sale(db: Session, data: SaleCreate, user_id: int):
    if not customer_repository.get(db, data.customer_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer not found")

    line_items = []
    total_amount = Decimal("0")
    for item in data.items:
        product = product_repository.get(db, item.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product {item.product_id} not found",
            )
        subtotal = product.price * item.quantity
        total_amount += subtotal
        line_items.append(
            {"product_id": item.product_id, "quantity": item.quantity, "subtotal": subtotal}
        )

    sale = sale_repository.create(
        db,
        {
            "customer_id": data.customer_id,
            "user_id": user_id,
            "log_type": data.log_type,
            "total_amount": total_amount,
        },
    )

    for line in line_items:
        line["sale_id"] = sale.id
        sale_item_repository.create(db, line)

    db.refresh(sale)
    return sale
