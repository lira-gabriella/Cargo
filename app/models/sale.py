from app.database import Base
import enum

from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class LogType(str, enum.Enum):
    IMPORT = "Import"
    EXPORT = "Export"
    TRANSIT = "Transit"


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    log_type = Column(SAEnum(LogType, name="log_type"), nullable=False)
    sale_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0)

    customer = relationship("Customer", back_populates="sales")
    user = relationship("User", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="sale", uselist=False)
    receipt = relationship("Receipt", back_populates="sale", uselist=False)
