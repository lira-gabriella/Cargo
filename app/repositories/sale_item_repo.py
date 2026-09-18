from sqlalchemy.orm import Session

from app.models.sale_item import SaleItem


class SaleItemRepository:
    def create(self, db: Session, data: dict):
        sale_item = SaleItem(**data)
        db.add(sale_item)
        db.commit()
        db.refresh(sale_item)
        return sale_item


sale_item_repository = SaleItemRepository()
