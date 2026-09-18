import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite://"

from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(client):
    user_data = {
        "username": "testuser",
        "password": "testpassword",
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 201, response.text
    return user_data


@pytest.fixture
def auth_headers(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"],
        },
    )
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture
def category(client, auth_headers):
    response = client.post(
        "/categories/",
        json={"category_name": "Beverages"},
        headers=auth_headers,
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture
def supplier(client, auth_headers):
    response = client.post(
        "/suppliers/",
        json={"supplier_name": "Test Supplier", "country": "Testland"},
        headers=auth_headers,
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture
def customer(client, auth_headers):
    response = client.post(
        "/customers/",
        json={
            "company_name": "Test Company",
            "tin_number": "TIN123456",
            "phone_number": "5551234567",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture
def product(client, auth_headers, category, supplier):
    response = client.post(
        "/products/",
        json={
            "service_name": "Test Product",
            "category_id": category["id"],
            "supplier_id": supplier["id"],
            "price": 50.00,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201, response.text
    return response.json()
