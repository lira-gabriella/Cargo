from fastapi.testclient import TestClient


def test_list_sales(client, auth_headers):
    response = client.get("/sales/", headers=auth_headers)
    assert response.status_code == 200, response.text


def test_create_sale(client, auth_headers, customer, product):
    sale_data = {
        "customer_id": customer["id"],
        "log_type": "Import",
        "items": [{"product_id": product["id"], "quantity": 2}],
    }
    response = client.post("/sales/", json=sale_data, headers=auth_headers)
    assert response.status_code == 201, response.text
    assert response.json()["customer_id"] == customer["id"]


def test_get_sale(client, auth_headers, customer, product):
    sale_data = {
        "customer_id": customer["id"],
        "log_type": "Export",
        "items": [{"product_id": product["id"], "quantity": 1}],
    }
    create_response = client.post("/sales/", json=sale_data, headers=auth_headers)
    assert create_response.status_code == 201, create_response.text
    sale_id = create_response.json()["id"]

    response = client.get(f"/sales/{sale_id}", headers=auth_headers)
    assert response.status_code == 200, response.text
    assert response.json()["id"] == sale_id
