import pytest
from faker import Faker
import unicodedata
fake = Faker('fr_CA')

@pytest.fixture(scope="module")
def user_data():
    # This function is used to normalize the first_name and last_name to be used as a password
    # Example: "Éric" -> "Eric"
    def normalize_string(input_str: str) -> str:
        normalized_str = unicodedata.normalize('NFKD', input_str)
        ascii_str = normalized_str.encode('ascii', 'ignore')
        return ascii_str.decode('ascii')

    first_name = fake.first_name()
    last_name = fake.last_name()
    password = "Cafepass1"
    email = normalize_string(first_name).replace(" ", "").lower() + "." + normalize_string(last_name).replace(" ", "").lower() + "@umontreal.ca"
    return {
            "email": email,
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
        "email": "cafesansfil@umontreal.ca",
        "matricule": "cs12345",
        "username": "cafesansfil",
        "password": "Cafepass1",
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
#       /api/users/{username}
# --------------------------------------

def test_get_user_success(client, list_users, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    username = list_users[0]["username"]
    response = client.get(f"/api/users/{username}", headers=headers)
    assert response.status_code == 200

def test_get_user_unauthorized(client, list_users):
    username = list_users[0]["username"]
    response = client.get(f"/api/users/{username}")
    assert response.status_code == 401

def test_get_user_not_found(client, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    username = "dont exist" # Non-existant username
    response = client.get(f"/api/users/{username}", headers=headers)
    assert response.status_code == 404

def test_update_user_success(client, list_users, user_data_cafesansfil, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    username = list_users[0]["username"]
    response = client.put(f"/api/users/{username}", json=user_data_cafesansfil, headers=headers)
    assert response.status_code == 200

def test_update_user_unauthorized(client, list_users, user_data_cafesansfil):
    username = list_users[0]["username"]
    response = client.put(f"/api/users/{username}", json=user_data_cafesansfil)
    assert response.status_code == 401

def test_update_user_forbidden(client, list_users, user_data_cafesansfil, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    username = list_users[1]["username"]
    response = client.put(f"/api/users/{username}", json=user_data_cafesansfil, headers=headers)
    assert response.status_code == 403

def test_update_user_not_found(client, user_data_cafesansfil, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    username = "dont exist" # Non-existant username
    response = client.put(f"/api/users/{username}", json=user_data_cafesansfil, headers=headers)
    assert response.status_code == 404
