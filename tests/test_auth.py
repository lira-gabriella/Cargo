from fastapi.testclient import TestClient


def test_register(client):
    user_data = {
        "username": "newuser",
        "password": "newpassword123",
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 201, response.text


def test_login(client, test_user):
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200, response.text
    assert "access_token" in response.json()


def test_login_wrong_password(client, test_user):
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "wrongpassword"},
    )
    assert response.status_code == 401, response.text
