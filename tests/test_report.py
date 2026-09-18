from fastapi.testclient import TestClient


def test_get_status_report(client, auth_headers, customer, product):
    sale_data = {
        "customer_id": customer["id"],
        "log_type": "Import",
        "items": [{"product_id": product["id"], "quantity": 2}],
    }
    create_response = client.post("/sales/", json=sale_data, headers=auth_headers)
    assert create_response.status_code == 201, create_response.text

    payment_data = {
        "sale_id": create_response.json()["id"],
        "method": "Cash",
        "amount_paid": 100.00,
    }
    client.post("/payments/", json=payment_data, headers=auth_headers)

    response = client.get("/reports/status", headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "total_sales" in data
    assert "total_revenue" in data
    assert "pending_payments" in data
