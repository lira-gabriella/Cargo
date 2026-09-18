from fastapi.testclient import TestClient


def test_create_product_missing_fields(client, auth_headers):
    response = client.post(
        "/products/",
        json={},
        headers=auth_headers,
    )
    assert response.status_code == 422, response.text


def test_create_product_negative_price(client, auth_headers, category, supplier):
    response = client.post(
        "/products/",
        json={
            "service_name": "Bad Product",
            "category_id": category["id"],
            "supplier_id": supplier["id"],
            "price": -10.00,
        },
        headers=auth_headers,
    )
    assert response.status_code == 422, response.text


def test_register_duplicate_username(client, test_user):
    user_data = {
        "username": "testuser",
        "password": "testpassword123",
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 409, response.text


def test_register_short_password(client):
    user_data = {
        "username": "shortpw",
        "password": "123",
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 422, response.text


def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "wrongpassword"},
    )
    assert response.status_code == 401, response.text


def test_create_category_empty_name(client, auth_headers):
    response = client.post(
        "/categories/",
        json={"category_name": ""},
        headers=auth_headers,
    )
    assert response.status_code == 422, response.text


def test_get_nonexistent_product(client, auth_headers):
    response = client.get("/products/9999", headers=auth_headers)
    assert response.status_code == 404, response.text


def test_get_nonexistent_category(client, auth_headers):
    response = client.get("/categories/9999", headers=auth_headers)
    assert response.status_code == 404, response.text


def test_get_nonexistent_supplier(client, auth_headers):
    response = client.get("/suppliers/9999", headers=auth_headers)
    assert response.status_code == 404, response.text


def test_get_nonexistent_customer(client, auth_headers):
    response = client.get("/customers/9999", headers=auth_headers)
    assert response.status_code == 404, response.text


def test_create_sale_missing_customer(client, auth_headers, product):
    response = client.post(
        "/sales/",
        json={
            "customer_id": 9999,
            "log_type": "Import",
            "items": [{"product_id": product["id"], "quantity": 1}],
        },
        headers=auth_headers,
    )
    assert response.status_code == 400, response.text


def test_create_sale_missing_product(client, auth_headers, customer):
    response = client.post(
        "/sales/",
        json={
            "customer_id": customer["id"],
            "log_type": "Import",
            "items": [{"product_id": 9999, "quantity": 1}],
        },
        headers=auth_headers,
    )
    assert response.status_code == 400, response.text


def test_payment_insufficient_amount(client, auth_headers, customer, product):
    sale_data = {
        "customer_id": customer["id"],
        "log_type": "Import",
        "items": [{"product_id": product["id"], "quantity": 2}],
    }
    create_response = client.post("/sales/", json=sale_data, headers=auth_headers)
    assert create_response.status_code == 201, create_response.text
    sale_id = create_response.json()["id"]

    response = client.post(
        "/payments/",
        json={
            "sale_id": sale_id,
            "method": "Cash",
            "amount_paid": 1.00,
        },
        headers=auth_headers,
    )
    assert response.status_code == 400, response.text


def test_record_payment_for_already_paid_sale(client, auth_headers, customer, product):
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

    response = client.post("/payments/", json=payment_data, headers=auth_headers)
    assert response.status_code == 409, response.text


def test_access_protected_route_without_auth(client):
    response = client.get("/products/")
    assert response.status_code == 401, response.text


def test_access_protected_route_with_invalid_token(client):
    response = client.get(
        "/products/",
        headers={"Authorization": "Bearer invalidtoken"},
    )
    assert response.status_code == 401, response.text
