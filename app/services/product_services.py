from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.product_repo import product_repository
from app.repositories.category_repo import category_repository
from app.repositories.supplier_repo import supplier_repository
from app.schemas.product import ProductCreate, ProductUpdate


def get_product(db: Session, id: int):
    product = product_repository.get(db, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


def list_products(db: Session):
    return product_repository.get_all(db)


def _validate_references(db: Session, category_id: int, supplier_id: int):
    if not category_repository.get(db, category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found"
        )
    if not supplier_repository.get(db, supplier_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Supplier not found"
        )


def create_product(db: Session, data: ProductCreate):
    _validate_references(db, data.category_id, data.supplier_id)
    return product_repository.create(db, data.model_dump())


def update_product(db: Session, product_id: int, data: ProductUpdate):
    product = get_product(db, product_id)
    update_data = data.model_dump(exclude_unset=True)
    if "category_id" in update_data or "supplier_id" in update_data:
        _validate_references(
            db,
            update_data.get("category_id", product.category_id),
            update_data.get("supplier_id", product.supplier_id),
        )
    return product_repository.update(db, product, update_data)


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    try:
        product_repository.delete(db, product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete a product that appears in existing sales",
        )
