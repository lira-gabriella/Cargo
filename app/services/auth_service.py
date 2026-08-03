from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from repositories.user_repo import user_repository
from schemas.user import UserCreate
from services.security import hash_password, verify_password, create_access_token


def register_user(db: Session, data: UserCreate):
    if user_repository.get_by_username(db, data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already taken"
        )
    payload = data.model_dump()
    payload["password"] = hash_password(payload["password"])
    return user_repository.create(db, payload)


def login(db: Session, username: str, password: str) -> str:
    user = user_repository.get_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return create_access_token(subject=str(user.id))
