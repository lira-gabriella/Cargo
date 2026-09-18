from fastapi.testclient import TestClient


def test_list_categories(client, auth_headers):
    response = client.get("/categories/", headers=auth_headers)
    assert response.status_code == 200, response.text


def test_get_category(client, auth_headers, category):
    response = client.get(f"/categories/{category['id']}", headers=auth_headers)
    assert response.status_code == 200, response.text


def test_create_category(client, auth_headers):
    response = client.post(
        "/categories/",
        json={"category_name": "Electronics"},
        headers=auth_headers,
    )
    assert response.status_code == 201, response.text


def test_update_category(client, auth_headers, category):
    response = client.put(
        f"/categories/{category['id']}",
        json={"category_name": "Updated Category"},
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text


def test_delete_category(client, auth_headers, category):
    response = client.delete(f"/categories/{category['id']}", headers=auth_headers)
    assert response.status_code == 204, response.text
