from fastapi.testclient import TestClient


def test_list_suppliers(client, auth_headers):
    response = client.get("/suppliers/", headers=auth_headers)
    assert response.status_code == 200, response.text


def test_get_supplier(client, auth_headers, supplier):
    response = client.get(f"/suppliers/{supplier['id']}", headers=auth_headers)
    assert response.status_code == 200, response.text


def test_create_supplier(client, auth_headers):
    response = client.post(
        "/suppliers/",
        json={"supplier_name": "New Supplier", "country": "India"},
        headers=auth_headers,
    )
    assert response.status_code == 201, response.text


def test_update_supplier(client, auth_headers, supplier):
    response = client.put(
        f"/suppliers/{supplier['id']}",
        json={"supplier_name": "Updated Supplier", "country": "Sri Lanka"},
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text


def test_delete_supplier(client, auth_headers, supplier):
    response = client.delete(f"/suppliers/{supplier['id']}", headers=auth_headers)
    assert response.status_code == 204, response.text
