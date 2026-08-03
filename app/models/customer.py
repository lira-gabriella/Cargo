from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    tin_number = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)

    sales = relationship("Sale", back_populates="customer")
