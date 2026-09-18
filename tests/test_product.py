from fastapi.testclient import TestClient


def test_list_products(client, auth_headers):
    response = client.get("/products/", headers=auth_headers)
    assert response.status_code == 200, response.text


def test_get_product(client, auth_headers, product):
    response = client.get(f"/products/{product['id']}", headers=auth_headers)
    assert response.status_code == 200, response.text


def test_create_product(client, auth_headers, category, supplier):
    product_data = {
        "service_name": "Coca Cola",
        "category_id": category["id"],
        "supplier_id": supplier["id"],
        "price": 100.00,
    }
    response = client.post("/products/", json=product_data, headers=auth_headers)
    assert response.status_code == 201, response.text
    assert response.json()["service_name"] == "Coca Cola"


def test_update_product(client, auth_headers, product):
    product_data = {"price": 75.00}
    response = client.put(
        f"/products/{product['id']}", json=product_data, headers=auth_headers
    )
    assert response.status_code == 200, response.text


def test_delete_product(client, auth_headers, product):
    response = client.delete(f"/products/{product['id']}", headers=auth_headers)
    assert response.status_code == 204, response.text
