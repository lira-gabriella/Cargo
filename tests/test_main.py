from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_list_products(client, auth_headers):
    response = client.get("/products/", headers=auth_headers)
    assert response.status_code == 200


def test_create_product(client, auth_headers, category, supplier):
    product_data = {
        "service_name": "Coca Cola",
        "category_id": category["id"],
        "supplier_id": supplier["id"],
        "price": 100.00,
    }
    response = client.post("/products/", json=product_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["service_name"] == "Coca Cola"
