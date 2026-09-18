
CARGO Ltd - Warehouse POS API
This is a custom B2B Point of Sale (POS) and inventory system built for CARGO Ltd, 
a public bonded warehouse in Kicukiro District, Kigali City, Rwanda.

The Problem
Right now, the warehouse manager records imports, exports, and storage records on paper.
This causes lost data, missing details, and makes creating weekly reports a nightmare.

Our Solution

Instead of a retail store setup that sells small items over a counter, this application is a service-based system.
It lets CARGO Ltd bill international cargo owners for warehouse space, logistics processing, and handling fees.
The API calculates rates automatically, handles multi-line checkouts
(like billing a truck carrying both chairs and beds at the same time), 
checks payments, and generates a unique digital gate pass for the truck drivers to leave the warehouse safely.


Tech Stack We UsedFramework:
FastAPI (for fast, easy routing)
Database:PostgreSQL (to keep all our records secure)
ORM: SQLAlchemy (to link our Python code to database tables)
Validation: Pydantic (to check input data before it hits the database)

How to Setup and Run This Locally

1. Download the Project

   Clone the repository and go into the project folder:git clone github.comcd cargo-pos-api

   2. Add Environment VariablesCreate a file named .env in the main folder and add your local PostgreSQL database URL link:DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/cargo_pos_db
  

   Create a Virtual Environment
   Create the uv venv env
   source env/bin/activate
   pip install -r requirements.txt
   then run fastapi dev
   clock on the link of the Go to http://localhost:8000/


   Quick Things to Test in Swagger UI
   1.Relational Safety Test: Try creating a service rate (POST /products/) but give it a category_id of 999 (which doesn't exist).
    The API will reject it with a 400 error because it prevents broken links in your data.
   
   2.Tax Check Test: Try creating two different customers using the exact same tin_number. The system will block the second one to keep customer profiles clean and accurate.
   
  3.Checkout & Gate Pass Test: Send a checkout payload to POST /sales with a mix of items. If the customer didn't pay enough money to cover the total bill, the transaction will fail.
  If they pay the correct amount, it succeeds and spits out a gate pass code like: gate_pass_code: KGL-GATE-IMPORT-A1B2C3D4.


Running Tests

The project uses Pytest with SQLite as the test database. The test environment is isolated from the PostgreSQL development database.

1. Activate the virtual environment

source env/bin/activate

2. Run all tests

PYTHONPATH=. pytest tests/

3. Run a specific test file

PYTHONPATH=. pytest tests/test_auth.py
PYTHONPATH=. pytest tests/test_category.py
PYTHONPATH=. pytest tests/test_supplier.py
PYTHONPATH=. pytest tests/test_customer.py
PYTHONPATH=. pytest tests/test_product.py
PYTHONPATH=. pytest tests/test_sale.py
PYTHONPATH=. pytest tests/test_payment.py
PYTHONPATH=. pytest tests/test_receipt.py
PYTHONPATH=. pytest tests/test_report.py
PYTHONPATH=. pytest tests/test_security.py
PYTHONPATH=. pytest tests/test_main.py

All tests use SQLite in-memory database and run independently. No PostgreSQL is required for tests.

   
