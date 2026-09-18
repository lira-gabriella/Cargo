from fastapi.testclient import TestClient


def test_record_payment(client, auth_headers, customer, product):
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
    response = client.post("/payments/", json=payment_data, headers=auth_headers)
    assert response.status_code == 201, response.text
    assert response.json()["sale_id"] == sale_id
