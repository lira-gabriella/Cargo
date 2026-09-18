from sqlalchemy.orm import Session

from app.models.sale import Sale


class SaleRepository:
    def get(self, db: Session, id: int):
        return db.get(Sale, id)

    def get_all(self, db: Session):
        return db.query(Sale).all()

    def create(self, db: Session, data: dict):
        sale = Sale(**data)
        db.add(sale)
        db.commit()
        db.refresh(sale)
        return sale


sale_repository = SaleRepository()
