# -----------------------------
#       /api/auth/login
# -----------------------------


def test_login_success(client):
    login_data = {
        "username": "7802085",
        "password": "Cafepass1",
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200


def test_login_unauthorized(client):
    login_data = {
        "username": "invalidusername",
        "password": "invalidpassword",
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 401


# -----------------------------
#       /api/auth/test-token
# -----------------------------


def test_test_token_success(client, auth_login):
    tokens = auth_login
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = client.post("/api/auth/test-token", headers=headers)
    assert response.status_code == 200


def test_test_token_unauthorized(client):
    response = client.post("/api/auth/test-token")
    assert response.status_code == 401


# -----------------------------
#      /api/auth/refresh
# -----------------------------


def test_refresh_success(client, auth_login):
    tokens = auth_login
    refresh_data = tokens["refresh_token"]
    headers = {"Content-Type": "application/json"}
    response = client.post("/api/auth/refresh", json=refresh_data, headers=headers)
    assert response.status_code == 200
