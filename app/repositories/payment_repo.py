from sqlalchemy.orm import Session

from models.payment import Payment


class PaymentRepository:
    def get(self, db: Session, id: int):
        return db.get(Payment, id)

    def get_all(self, db: Session):
        return db.query(Payment).all()

    def create(self, db: Session, data: dict):
        payment = Payment(**data)
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment


payment_repository = PaymentRepository()
