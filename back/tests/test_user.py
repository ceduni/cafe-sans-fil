import pytest
from faker import Faker
fake = Faker('fr_CA')

@pytest.fixture(scope="module")
def user_data():
    first_name = fake.first_name()
    last_name = fake.last_name()
    password= "Password1"
    return {
            "email": "sonofgocou@hotmail.com",
            "matricule": fake.bothify(text='??#####').lower(),
            "username": fake.user_name(),
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "photo_url": fake.image_url(width=200, height=200)
    }

@pytest.fixture(scope="module")
def user_data_cafesansfil():
    return {
        "email": "spider@man.com",
        "matricule": "sm12345",
        "username": "CafeSansfil1",
        "password": "CafeSansfil1",
        "first_name": "Tom",
        "last_name": "Holland",
        "photo_url": "https://i.pinimg.com/originals/50/c0/88/50c0883ae3c0e6be1213407c2b746177.jpg"
    }

# --------------------------------------
#       /api/users
# --------------------------------------

def test_list_users_success(client, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    response = client.get("/api/users?sort=name", headers=headers)
    assert response.status_code == 200

def test_list_users_unauthorized(client):
    response = client.get("/api/users?sort=name")
    assert response.status_code == 401

def test_create_user_success(client, user_data):
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 200

def test_create_user_conflict(client, user_data_cafesansfil):
    response = client.post("/api/users", json=user_data_cafesansfil)
    assert response.status_code == 409

# --------------------------------------
#       /api/users/{user_id}
# --------------------------------------

def test_get_user_success(client, list_users, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    user_id = list_users[0]["user_id"]
    response = client.get(f"/api/users/{user_id}", headers=headers)
    assert response.status_code == 200

def test_get_user_unauthorized(client, list_users):
    user_id = list_users[0]["user_id"]
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 401

def test_get_user_not_found(client, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    user_id = "123e4567-e89b-12d3-a456-426614173999"  # Non-existent ID
    response = client.get(f"/api/users/{user_id}", headers=headers)
    assert response.status_code == 404

def test_update_user_success(client, list_users, user_data_cafesansfil, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    user_id = list_users[0]["user_id"]
    response = client.put(f"/api/users/{user_id}", json=user_data_cafesansfil, headers=headers)
    assert response.status_code == 200

def test_update_user_unauthorized(client, list_users, user_data_cafesansfil):
    user_id = list_users[0]["user_id"]
    response = client.put(f"/api/users/{user_id}", json=user_data_cafesansfil)
    assert response.status_code == 401

def test_update_user_forbidden(client, list_users, user_data_cafesansfil, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    user_id = list_users[1]["user_id"]
    response = client.put(f"/api/users/{user_id}", json=user_data_cafesansfil, headers=headers)
    assert response.status_code == 403

def test_update_user_not_found(client, user_data_cafesansfil, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    user_id = "123e4567-e89b-12d3-a456-426614173999"  # Non-existent ID
    response = client.put(f"/api/users/{user_id}", json=user_data_cafesansfil, headers=headers)
    assert response.status_code == 404
