import pytest
from faker import Faker
fake = Faker('fr_CA')

@pytest.fixture(scope="function")
def cafe_data():
    return {
            "name": fake.company(),
            "description": "Un café populaire près de la bibliothèque principale.",
            "image_url": "https://media.architecturaldigest.com/photos/5b083c4675a4f940de3da8f1/master/pass/case-study-coffee.jpg",
            "faculty": "Science",
            "location": {
                "pavillon": "Pavillon JEAN-TALON",
                "local": "local B-1234"
            },
            "is_open": True,
            "opening_hours": [
                {"day": "Lundi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Mardi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Mercredi", "blocks": [{"start": "09:00", "end": "12:00"}, {"start": "13:00", "end": "17:00"}]},
                {"day": "Jeudi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Vendredi", "blocks": [{"start": "10:00", "end": "11:00"}, {"start": "12:00", "end": "17:00"}]}
            ],
            "contact": {
                "email": "central@cafe.com",
                "phone_number": "+123456789",
                "website": "http://centralcafe.com"
            },
            "social_media": [{"platform_name": "Facebook", "link": "http://fb.com/centralcafe"}],
            "payment_methods": [{"method": "Carte de Crédit", "minimum": 4.0}],
            "staff": [
                {"user_id": "15df2842-fc31-4107-99bf-3cb7b0b5baf5", "role": "Admin"},
                {"user_id": "3c0cda2b-26f3-4cc8-8e84-0c81bf84e8f9", "role": "Admin"},
                {"user_id": "a1e63c28-7e5b-4d12-8cf2-8c7875191d2b", "role": "Bénévole"},
                {"user_id": "5a0e7b25-1722-41aa-8eeb-25dfedc2c1ae", "role": "Bénévole"},
                {"user_id": "9c42c791-4b0a-4170-bb8a-2c1f4462cf33", "role": "Bénévole"},
                {"user_id": "e8c5de06-7d98-4d66-89a3-8c37e3b16bd5", "role": "Bénévole"}
            ],
            "menu_items": [
                {
                    "name": "Cheeseburger " + fake.word(),
                    "tags": ["Rapide", "Savoureux"],
                    "description": "Un délicieux cheeseburger avec laitue, tomate et fromage",
                    "image_url": "https://thedelightfullaugh.com/wp-content/uploads/2020/09/smashed-double-cheeseburger.jpg",
                    "price": 5.99,
                    "is_available": True,
                    "category": "Burgers",
                    "options": [
                        {"type": "taille", "value": "grand", "fee": 0.5},
                        {"type": "ingrédients", "value": "bœuf", "fee": 0},
                        {"type": "ingrédients", "value": "laitue", "fee": 0},
                        {"type": "ingrédients", "value": "tomate", "fee": 0},
                        {"type": "ingrédients", "value": "fromage", "fee": 0}
                    ]
                },
                {
                    "name": "Chicken Caesar Salad",
                    "tags": ["Léger", "Fraîcheur"],
                    "description": "Une salade César avec du poulet grillé, de la laitue romaine et de la vinaigrette César",
                    "image_url": None,
                    "price": 7.99,
                    "is_available": False,
                    "category": "Salads",
                    "options": []
                }
            ],
            "additional_info": [
                {
                    "type": "promo",
                    "value": "10% de réduction les lundis",
                    "start": "2023-01-01T00:00:00.000Z",
                    "end": "2023-01-02T00:00:00.000Z"
                }
            ]
    }

@pytest.fixture(scope="function")
def cafe_data2():
    return {
            "additional_info": [
                {
                    "type": "promo",
                    "value": "10% de réduction les lundis " + fake.word(),
                    "start": "2023-01-01T00:00:00.000Z",
                    "end": "2023-01-02T00:00:00.000Z"
                }
            ]
    }

# -----------------------------
#       /api/cafes
# -----------------------------

def test_list_cafes_success(client):
    response = client.get("/api/cafes")
    assert response.status_code == 200

def test_create_cafe_success(client, cafe_data, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    response = client.post("/api/cafes", json=cafe_data, headers=headers)
    assert response.status_code == 200

def test_create_cafe_unauthorized(client, cafe_data):
    response = client.post("/api/cafes", json=cafe_data)
    assert response.status_code == 401

# --------------------------------------
#       /api/cafes/{cafe_id}
# --------------------------------------

def test_get_cafe_success(client, list_cafes):
    cafe_id = list_cafes[0]["cafe_id"]
    response = client.get(f"/api/cafes/{cafe_id}")
    assert response.status_code == 200

def test_get_cafe_not_found(client):
    cafe_id = "123e4567-e89b-12d3-a456-426614173999"  # Non-existent ID
    response = client.get(f"/api/cafes/{cafe_id}")
    assert response.status_code == 404  

def test_update_cafe_success(client, list_cafes, cafe_data2, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_id = list_cafes[0]["cafe_id"]
    response = client.put(f"/api/cafes/{cafe_id}", json=cafe_data2, headers=headers)
    assert response.status_code == 200

def test_update_cafe_unauthorized(client, list_cafes, cafe_data2):
    cafe_id = list_cafes[0]["cafe_id"]
    response = client.put(f"/api/cafes/{cafe_id}", json=cafe_data2)
    assert response.status_code == 401

def test_update_cafe_forbidden(client, list_cafes, cafe_data2, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_id = list_cafes[1]["cafe_id"]
    response = client.put(f"/api/cafes/{cafe_id}", json=cafe_data2, headers=headers)
    assert response.status_code == 403

def test_update_cafe_not_found(client, cafe_data2, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_id = "123e4567-e89b-12d3-a456-426614173999"  # Non-existent ID
    response = client.put(f"/api/cafes/{cafe_id}", json=cafe_data2, headers=headers)
    assert response.status_code == 404

# --------------------------------------
#       /api/cafes/{cafe_id}/menu
# --------------------------------------

def test_list_menu_items_success(client, list_cafes):
    cafe_id = list_cafes[0]["cafe_id"]
    response = client.get(f"/api/cafes/{cafe_id}/menu")
    assert response.status_code == 200

def test_list_menu_items_not_found(client):
    cafe_id = "123e4567-e89b-12d3-a456-426614173999"  # Non-existent ID
    response = client.get(f"/api/cafes/{cafe_id}/menu")
    assert response.status_code == 404

def test_create_menu_item_success(client, list_cafes, cafe_data, auth_login):
    menu_item_data = cafe_data["menu_items"][0]
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_id = list_cafes[0]["cafe_id"]
    response = client.post(f"/api/cafes/{cafe_id}/menu", json=menu_item_data, headers=headers)
    assert response.status_code == 200

def test_create_menu_item_unauthorized(client, list_cafes, cafe_data):
    cafe_id = list_cafes[0]["cafe_id"]
    response = client.post(f"/api/cafes/{cafe_id}/menu", json=cafe_data)
    assert response.status_code == 401

def test_create_menu_item_forbidden(client, list_cafes, cafe_data, auth_login):
    menu_item_data = cafe_data["menu_items"][0]
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_id = list_cafes[1]["cafe_id"]
    response = client.post(f"/api/cafes/{cafe_id}/menu", json=menu_item_data, headers=headers)
    assert response.status_code == 403

def test_create_menu_item_not_found(client, cafe_data, auth_login):
    menu_item_data = cafe_data["menu_items"][0]
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_id = "123e4567-e89b-12d3-a456-426614173999"  # Non-existent ID
    response = client.post(f"/api/cafes/{cafe_id}/menu", json=menu_item_data, headers=headers)
    assert response.status_code == 404

# ------------------------------------------
#       /api/cafes/{cafe_id}/menu/{item_id}
# ------------------------------------------

def test_get_menu_item_success(client, list_cafes):
    cafe_id = list_cafes[0]["cafe_id"]
    item_id = list_cafes[0]["menu_items"][0]["item_id"]
    response = client.get(f"/api/cafes/{cafe_id}/menu/{item_id}")
    assert response.status_code == 200

def test_get_menu_item_not_found1(client, list_cafes):
    cafe_id = "123e4567-e89b-12d3-a456-426614173999"  # Non-existent ID
    item_id = list_cafes[0]["menu_items"][0]["item_id"]
    response = client.get(f"/api/cafes/{cafe_id}/menu/{item_id}")
    assert response.status_code == 404

def test_get_menu_item_not_found2(client, list_cafes):
    cafe_id = list_cafes[0]["cafe_id"]
    item_id = "123e4567-e89b-12d3-a456-426614173999"  # Non-existent ID
    response = client.get(f"/api/cafes/{cafe_id}/menu/{item_id}")
    assert response.status_code == 404

def test_update_menu_item_success(client, list_cafes, cafe_data, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_id = list_cafes[0]["cafe_id"]
    item_id = list_cafes[0]["menu_items"][0]["item_id"]
    menu_item_data = cafe_data["menu_items"][0]
    response = client.put(f"/api/cafes/{cafe_id}/menu/{item_id}", json=menu_item_data, headers=headers)
    assert response.status_code == 200

def test_update_menu_item_unauthorized(client, list_cafes, cafe_data):
    cafe_id = list_cafes[0]["cafe_id"]
    item_id = list_cafes[0]["menu_items"][0]["item_id"]
    menu_item_data = cafe_data["menu_items"][0]
    response = client.put(f"/api/cafes/{cafe_id}/menu/{item_id}", json=menu_item_data)
    assert response.status_code == 401

def test_update_menu_item_forbidden(client, list_cafes, cafe_data, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_id = list_cafes[1]["cafe_id"]
    item_id = list_cafes[0]["menu_items"][0]["item_id"]
    menu_item_data = cafe_data["menu_items"][0]
    response = client.put(f"/api/cafes/{cafe_id}/menu/{item_id}", json=menu_item_data, headers=headers)
    assert response.status_code == 403

def test_update_menu_item_not_found1(client, list_cafes, cafe_data, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_id = "123e4567-e89b-12d3-a456-426614173999"  # Non-existent ID
    item_id = list_cafes[0]["menu_items"][0]["item_id"]
    menu_item_data = cafe_data["menu_items"][0]
    response = client.put(f"/api/cafes/{cafe_id}/menu/{item_id}", json=menu_item_data, headers=headers)
    assert response.status_code == 404

def test_update_menu_item_not_found2(client, list_cafes, cafe_data, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_id = list_cafes[0]["cafe_id"]
    item_id = "123e4567-e89b-12d3-a456-426614173999"  # Non-existent ID
    menu_item_data = cafe_data["menu_items"][0]
    response = client.put(f"/api/cafes/{cafe_id}/menu/{item_id}", json=menu_item_data, headers=headers)
    assert response.status_code == 404

def test_delete_menu_item_success(client, list_cafes, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_id = list_cafes[0]["cafe_id"]
    item_id = list_cafes[0]["menu_items"][0]["item_id"]
    response = client.delete(f"/api/cafes/{cafe_id}/menu/{item_id}", headers=headers)
    assert response.status_code == 200

def test_delete_menu_item_unauthorized(client, list_cafes):
    cafe_id = list_cafes[0]["cafe_id"]
    item_id = list_cafes[0]["menu_items"][0]["item_id"]
    response = client.delete(f"/api/cafes/{cafe_id}/menu/{item_id}")
    assert response.status_code == 401

def test_delete_menu_item_forbidden(client, list_cafes, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_id = list_cafes[1]["cafe_id"]
    item_id = list_cafes[0]["menu_items"][0]["item_id"]
    response = client.delete(f"/api/cafes/{cafe_id}/menu/{item_id}", headers=headers)
    assert response.status_code == 403

def test_delete_menu_item_not_found1(client, list_cafes, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_id = "123e4567-e89b-12d3-a456-426614173999"  # Non-existent ID
    item_id = list_cafes[0]["menu_items"][0]["item_id"]
    response = client.delete(f"/api/cafes/{cafe_id}/menu/{item_id}", headers=headers)
    assert response.status_code == 404

def test_delete_menu_item_not_found2(client, list_cafes, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_id = list_cafes[0]["cafe_id"]
    item_id = "123e4567-e89b-12d3-a456-426614173999"  # Non-existent ID
    response = client.delete(f"/api/cafes/{cafe_id}/menu/{item_id}", headers=headers)
    assert response.status_code == 404

# -----------------------------
#       /api/search
# -----------------------------

def test_search(client):
    response = client.get("/api/search?query=cafe&sort=name")
    assert response.status_code == 200
