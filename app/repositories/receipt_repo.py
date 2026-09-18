from sqlalchemy.orm import Session

from app.models.receipt import Receipt


class ReceiptRepository:
    def get(self, db: Session, id: int):
        return db.get(Receipt, id)

    def get_by_sale(self, db: Session, sale_id: int):
        return db.query(Receipt).filter(Receipt.sale_id == sale_id).first()

    def create(self, db: Session, data: dict):
        receipt = Receipt(**data)
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        return receipt


receipt_repository = ReceiptRepository()
