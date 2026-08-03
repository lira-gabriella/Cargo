from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    supplier_name = Column(String, nullable=False)
    country = Column(String, nullable=False)

    products = relationship("Product", back_populates="supplier")
