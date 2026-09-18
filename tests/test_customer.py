from fastapi.testclient import TestClient


def test_list_customers(client, auth_headers):
    response = client.get("/customers/", headers=auth_headers)
    assert response.status_code == 200, response.text


def test_get_customer(client, auth_headers, customer):
    response = client.get(f"/customers/{customer['id']}", headers=auth_headers)
    assert response.status_code == 200, response.text


def test_create_customer(client, auth_headers):
    response = client.post(
        "/customers/",
        json={
            "company_name": "New Company",
            "tin_number": "TIN789",
            "phone_number": "9876543210",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201, response.text


def test_update_customer(client, auth_headers, customer):
    response = client.put(
        f"/customers/{customer['id']}",
        json={"company_name": "Updated Company"},
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text


def test_delete_customer(client, auth_headers, customer):
    response = client.delete(f"/customers/{customer['id']}", headers=auth_headers)
    assert response.status_code == 204, response.text
