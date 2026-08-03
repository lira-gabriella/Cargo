from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from routers.auth import get_current_user
from schemas.sale import SaleCreate, SaleRead
from services import sale_service

router = APIRouter(prefix="/sales", tags=["sales"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[SaleRead])
def list_sales(db: Session = Depends(get_db)):
    return sale_service.list_sales(db)


@router.get("/{sale_id}", response_model=SaleRead)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    return sale_service.get_sale(db, sale_id)


@router.post("/", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
def create_sale(
    data: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return sale_service.create_sale(db, data, user_id=current_user.id)
