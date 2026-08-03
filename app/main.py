from fastapi import FastAPI

import models
from database import Base, engine
from routers import auth, category, customer, payment, product, receipt, report, sale, supplier

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CARGO Ltd POS API", version="1")

app.include_router(auth.router)
app.include_router(category.router)
app.include_router(supplier.router)
app.include_router(customer.router)
app.include_router(product.router)
app.include_router(sale.router)
app.include_router(payment.router)
app.include_router(receipt.router)
app.include_router(report.router)
