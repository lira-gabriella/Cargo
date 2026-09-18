from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repo import user_repository
from app.schemas.user import Token, UserCreate, UserRead
from app.services import auth_service
from app.services.security import oauth2_scheme

router = APIRouter(tags=["auth"])


@router.post("/users/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register_user(db, data)


@router.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = auth_service.login(db, form_data.username, form_data.password)
    return Token(access_token=token)
