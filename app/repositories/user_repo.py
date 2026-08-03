from sqlalchemy.orm import Session

from models.user import User


class UserRepository:
    def get(self, db: Session, id: int):
        return db.get(User, id)

    def get_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def get_all(self, db: Session):
        return db.query(User).all()

    def create(self, db: Session, data: dict):
        user = User(**data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


user_repository = UserRepository()
