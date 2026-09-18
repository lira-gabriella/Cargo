from fastapi.testclient import TestClient


def test_get_receipt(client, auth_headers, customer, product):
    sale_data = {
        "customer_id": customer["id"],
        "log_type": "Import",
        "items": [{"product_id": product["id"], "quantity": 2}],
    }
    create_response = client.post("/sales/", json=sale_data, headers=auth_headers)
    assert create_response.status_code == 201, create_response.text
    sale_id = create_response.json()["id"]

    payment_data = {
        "sale_id": sale_id,
        "method": "Cash",
        "amount_paid": 100.00,
    }
    client.post("/payments/", json=payment_data, headers=auth_headers)

    by_sale_response = client.get(
        f"/receipts/by-sale/{sale_id}", headers=auth_headers
    )
    assert by_sale_response.status_code == 200, by_sale_response.text
    receipt_id = by_sale_response.json()["id"]

    response = client.get(f"/receipts/{receipt_id}", headers=auth_headers)
    assert response.status_code == 200, response.text
    assert response.json()["id"] == receipt_id


def test_get_receipt_by_sale(client, auth_headers, customer, product):
    sale_data = {
        "customer_id": customer["id"],
        "log_type": "Import",
        "items": [{"product_id": product["id"], "quantity": 2}],
    }
    create_response = client.post("/sales/", json=sale_data, headers=auth_headers)
    assert create_response.status_code == 201, create_response.text
    sale_id = create_response.json()["id"]

    payment_data = {
        "sale_id": sale_id,
        "method": "Cash",
        "amount_paid": 100.00,
    }
    payment_response = client.post(
        "/payments/", json=payment_data, headers=auth_headers
    )
    assert payment_response.status_code == 201, payment_response.text

    response = client.get(f"/receipts/by-sale/{sale_id}", headers=auth_headers)
    assert response.status_code == 200, response.text
