import pytest
import random

@pytest.fixture(scope="module")
def order_data():
    return {
            "cafe_slug": "tore-et-fraction",
            "items": [
                {
                    "item_slug": "croissant",
                    "quantity": 2 + random.randint(0, 3),
                    "item_price": 2.99,
                    "options": [
                        {"type": "taille", "value": "moyenne", "fee": 0.50},
                        {"type": "fromage supplémentaire", "value": "oui", "fee": 1.00}
                    ]
                },
                {
                    "item_slug": "baguette",
                    "quantity": 1,
                    "item_price": 4.99,
                    "options": [
                        {"type": "taille", "value": "grande", "fee": 1.00},
                        {"type": "sauce supplémentaire", "value": "non", "fee": 0.00}
                    ]
                }
            ]
    }

@pytest.fixture(scope="module")
def order_data2():
    return {
            "items": [
                {
                    "item_slug": "croissant",
                    "quantity": 2 + random.randint(0, 3),
                    "item_price": 2.99,
                    "options": [
                        {"type": "taille", "value": "moyenne", "fee": 0.50},
                        {"type": "fromage supplémentaire", "value": "oui", "fee": 1.00}
                    ]
                },
                {
                    "item_slug": "baguette",
                    "quantity": 1,
                    "item_price": 4.99,
                    "options": [
                        {"type": "taille", "value": "grande", "fee": 1.00},
                        {"type": "sauce supplémentaire", "value": "non", "fee": 0.00}
                    ]
                }
            ]
    }

# --------------------------------------
#       /api/orders
# --------------------------------------

def test_list_orders_success(client, auth_login):
    tokens = auth_login
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = client.get("/api/orders?sort_by=-order_number&page=1&limit=10", headers=headers)
    assert response.status_code == 200

def test_list_orders_unauthorized(client):
    response = client.get("/api/orders")
    assert response.status_code == 401

def test_create_order_success(client, list_cafes, auth_login, order_data):
    tokens = auth_login
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    order_data["cafe_slug"] = list_cafes[0]["slug"]
    response = client.post("/api/orders", json=order_data, headers=headers)
    assert response.status_code == 200

def test_create_order_unauthorized(client, order_data):
    response = client.post("/api/orders", json=order_data)
    assert response.status_code == 401

def test_create_order_not_found(client, auth_login, order_data):
    tokens = auth_login
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    order_data["cafe_slug"] = "Non existent Cafe"
    response = client.post("/api/orders", json=order_data, headers=headers)
    assert response.status_code == 404

# --------------------------------------
#       /api/orders{order_id}
# --------------------------------------

def test_get_order_success(client, list_orders, auth_login):
    tokens = auth_login
    order_id = list_orders[0]["order_id"]
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = client.get(f"/api/orders/{order_id}", headers=headers)
    assert response.status_code == 200

def test_get_order_unauthorized(client, list_orders):
    order_id = list_orders[0]["order_id"]
    response = client.get(f"/api/orders/{order_id}")
    assert response.status_code == 401

def test_get_order_forbidden(client, list_orders, auth_login):
    tokens = auth_login
    order_id = list_orders[1]["order_id"]
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = client.get(f"/api/orders/{order_id}", headers=headers)
    assert response.status_code == 403

def test_get_order_not_found(client, auth_login):
    tokens = auth_login
    order_id = "123e4567-e89b-12d3-a456-426614173999"  # Non-existent ID
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = client.get(f"/api/orders/{order_id}", headers=headers)
    assert response.status_code == 404

def test_update_order_success(client, list_orders, order_data2, auth_login):
    tokens = auth_login
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    order_id = list_orders[0]["order_id"]
    response = client.put(f"/api/orders/{order_id}", json=order_data2, headers=headers)
    assert response.status_code == 200

def test_update_order_unauthorized(client, list_orders, order_data2):
    order= list_orders[0]["order_id"]
    response = client.put(f"/api/orders/{order}", json=order_data2)
    assert response.status_code == 401

def test_update_order_forbidden(client, list_orders, order_data2, auth_login):
    tokens = auth_login
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    order_id = list_orders[1]["order_id"]
    response = client.put(f"/api/orders/{order_id}", json=order_data2, headers=headers)
    assert response.status_code == 403

def test_update_order_not_found(client, order_data2, auth_login):
    tokens = auth_login
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    order_id = "123e4567-e89b-12d3-a456-426614173999"  # Non-existent ID
    response = client.put(f"/api/orders/{order_id}", json=order_data2, headers=headers)
    assert response.status_code == 404

# --------------------------------------
#       /api/orders{username}/orders
# --------------------------------------

def test_list_user_orders_success(client, list_users, auth_login):
    tokens = auth_login
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    username = list_users[0]["username"]
    response = client.get(f"/api/users/{username}/orders", headers=headers)
    assert response.status_code == 200

def test_list_user_orders_unauthorized(client, list_users):
    username = list_users[0]["username"]
    response = client.get(f"/api/users/{username}/orders")
    assert response.status_code == 401

def test_list_user_orders_forbidden(client, list_users, auth_login):
    tokens = auth_login
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    username = list_users[1]["username"]
    response = client.get(f"/api/users/{username}/orders", headers=headers)
    assert response.status_code == 403

# --------------------------------------
#       /api/orders{cafe_slug}/orders
# --------------------------------------

def test_list_cafe_orders_success(client, list_cafes, auth_login):
    tokens = auth_login
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    cafe_slug = list_cafes[0]["slug"]
    response = client.get(f"/api/cafes/{cafe_slug}/orders", headers=headers)
    assert response.status_code == 200

def test_list_cafe_orders_unauthorized(client, list_cafes):
    cafe_slug = list_cafes[0]["slug"]
    response = client.get(f"/api/cafes/{cafe_slug}/orders")
    assert response.status_code == 401

def test_list_cafe_orders_success(client, list_cafes, auth_login):
    tokens = auth_login
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    cafe_slug = list_cafes[1]["slug"]
    response = client.get(f"/api/cafes/{cafe_slug}/orders", headers=headers)
    assert response.status_code == 403