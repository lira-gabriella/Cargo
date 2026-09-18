from fastapi import Depends, HTTPException, status, Security
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repo import user_repository
from app.services.security import decode_access_token, oauth2_scheme


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = decode_access_token(token)
    except JWTError:
        raise credentials_error
    user = user_repository.get(db, int(user_id))
    if not user:
        raise credentials_error
    return user
