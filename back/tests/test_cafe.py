import pytest
from faker import Faker
fake = Faker('fr_CA')

@pytest.fixture(scope="module")
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
                {"username": fake.user_name(), "role": "Admin"},
                {"username": fake.user_name(), "role": "Admin"},
                {"username": fake.user_name(), "role": "Bénévole"},
                {"username": fake.user_name(), "role": "Bénévole"},
                {"username": fake.user_name(), "role": "Bénévole"},
                {"username": fake.user_name(), "role": "Bénévole"},
            ],
            "menu_items": [
                {
                    "name": "Cheeseburger " + fake.word(),
                    "tags": ["Rapide", "Savoureux"],
                    "description": "Un délicieux cheeseburger avec laitue, tomate et fromage",
                    "image_url": "https://thedelightfullaugh.com/wp-content/uploads/2020/09/smashed-double-cheeseburger.jpg",
                    "price": 5.99,
                    "in_stock": True,
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
                    "in_stock": False,
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

@pytest.fixture(scope="module")
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
    response = client.get("/api/cafes?is_open=true&sort_by=-name&page=1&limit=10")
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
#       /api/cafes/{cafe_slug}
# --------------------------------------

def test_get_cafe_success(client, list_cafes):
    cafe_slug = list_cafes[0]["slug"]
    response = client.get(f"/api/cafes/{cafe_slug}")
    assert response.status_code == 200

def test_get_cafe_not_found(client):
    cafe_slug = "dont exist" # Non-existant slug
    response = client.get(f"/api/cafes/{cafe_slug}")
    assert response.status_code == 404  

def test_update_cafe_success(client, list_cafes, cafe_data2, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = list_cafes[0]["slug"]
    response = client.put(f"/api/cafes/{cafe_slug}", json=cafe_data2, headers=headers)
    assert response.status_code == 200

def test_update_cafe_unauthorized(client, list_cafes, cafe_data2):
    cafe_slug = list_cafes[0]["slug"]
    response = client.put(f"/api/cafes/{cafe_slug}", json=cafe_data2)
    assert response.status_code == 401

def test_update_cafe_forbidden(client, list_cafes, cafe_data2, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = list_cafes[1]["slug"]
    response = client.put(f"/api/cafes/{cafe_slug}", json=cafe_data2, headers=headers)
    assert response.status_code == 403

def test_update_cafe_not_found(client, cafe_data2, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = "dont exist" # Non-existant slug
    response = client.put(f"/api/cafes/{cafe_slug}", json=cafe_data2, headers=headers)
    assert response.status_code == 404

# --------------------------------------
#       /api/cafes/{cafe_slug}/menu
# --------------------------------------

def test_list_menu_items_success(client, list_cafes):
    cafe_slug = list_cafes[0]["slug"]
    response = client.get(f"/api/cafes/{cafe_slug}/menu")
    assert response.status_code == 200

def test_list_menu_items_not_found(client):
    cafe_slug = "dont exist" # Non-existant slug
    response = client.get(f"/api/cafes/{cafe_slug}/menu")
    assert response.status_code == 404

def test_create_menu_item_success(client, list_cafes, cafe_data, auth_login):
    menu_item_data = cafe_data["menu_items"][0]
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = list_cafes[0]["slug"]
    response = client.post(f"/api/cafes/{cafe_slug}/menu", json=menu_item_data, headers=headers)
    assert response.status_code == 200

def test_create_menu_item_unauthorized(client, list_cafes, cafe_data):
    cafe_slug = list_cafes[0]["slug"]
    response = client.post(f"/api/cafes/{cafe_slug}/menu", json=cafe_data)
    assert response.status_code == 401

def test_create_menu_item_forbidden(client, list_cafes, cafe_data, auth_login):
    menu_item_data = cafe_data["menu_items"][0]
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = list_cafes[1]["slug"]
    response = client.post(f"/api/cafes/{cafe_slug}/menu", json=menu_item_data, headers=headers)
    assert response.status_code == 403

def test_create_menu_item_not_found(client, cafe_data, auth_login):
    menu_item_data = cafe_data["menu_items"][0]
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = "dont exist" # Non-existant slug
    response = client.post(f"/api/cafes/{cafe_slug}/menu", json=menu_item_data, headers=headers)
    assert response.status_code == 404

# ------------------------------------------
#       /api/cafes/{cafe_slug}/menu/{item_slug}
# ------------------------------------------

def test_get_menu_item_success(client, list_cafes):
    cafe_slug = list_cafes[0]["slug"]
    item_slug = list_cafes[0]["menu_items"][0]["slug"]
    response = client.get(f"/api/cafes/{cafe_slug}/menu/{item_slug}")
    assert response.status_code == 200

def test_get_menu_item_not_found1(client, list_cafes):
    cafe_slug = "dont exist" # Non-existant slug
    item_slug = list_cafes[0]["menu_items"][0]["slug"]
    response = client.get(f"/api/cafes/{cafe_slug}/menu/{item_slug}")
    assert response.status_code == 404

def test_get_menu_item_not_found2(client, list_cafes):
    cafe_slug = list_cafes[0]["slug"]
    item_slug = "dont exist" # Non-existant slug
    response = client.get(f"/api/cafes/{cafe_slug}/menu/{item_slug}")
    assert response.status_code == 404

def test_update_menu_item_success(client, list_cafes, cafe_data, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = list_cafes[0]["slug"]
    item_slug = list_cafes[0]["menu_items"][3]["slug"]
    menu_item_data = cafe_data["menu_items"][0]
    response = client.put(f"/api/cafes/{cafe_slug}/menu/{item_slug}", json=menu_item_data, headers=headers)
    assert response.status_code == 200

def test_update_menu_item_unauthorized(client, list_cafes, cafe_data):
    cafe_slug = list_cafes[0]["slug"]
    item_slug = list_cafes[0]["menu_items"][3]["slug"]
    menu_item_data = cafe_data["menu_items"][0]
    response = client.put(f"/api/cafes/{cafe_slug}/menu/{item_slug}", json=menu_item_data)
    assert response.status_code == 401

def test_update_menu_item_forbidden(client, list_cafes, cafe_data, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = list_cafes[1]["slug"]
    item_slug = list_cafes[0]["menu_items"][3]["slug"]
    menu_item_data = cafe_data["menu_items"][0]
    response = client.put(f"/api/cafes/{cafe_slug}/menu/{item_slug}", json=menu_item_data, headers=headers)
    assert response.status_code == 403

def test_update_menu_item_not_found1(client, list_cafes, cafe_data, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = "dont exist" # Non-existant slug
    item_slug = list_cafes[0]["menu_items"][3]["slug"]
    menu_item_data = cafe_data["menu_items"][0]
    response = client.put(f"/api/cafes/{cafe_slug}/menu/{item_slug}", json=menu_item_data, headers=headers)
    assert response.status_code == 404

def test_update_menu_item_not_found2(client, list_cafes, cafe_data, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = list_cafes[0]["slug"]
    item_slug = "dont exist" # Non-existant slug
    menu_item_data = cafe_data["menu_items"][0]
    response = client.put(f"/api/cafes/{cafe_slug}/menu/{item_slug}", json=menu_item_data, headers=headers)
    assert response.status_code == 404

def test_delete_menu_item_success(client, list_cafes, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = list_cafes[0]["slug"]
    item_slug = list_cafes[0]["menu_items"][0]["slug"]
    response = client.delete(f"/api/cafes/{cafe_slug}/menu/{item_slug}", headers=headers)
    assert response.status_code == 200

def test_delete_menu_item_unauthorized(client, list_cafes):
    cafe_slug = list_cafes[0]["slug"]
    item_slug = list_cafes[0]["menu_items"][0]["slug"]
    response = client.delete(f"/api/cafes/{cafe_slug}/menu/{item_slug}")
    assert response.status_code == 401

def test_delete_menu_item_forbidden(client, list_cafes, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = list_cafes[1]["slug"]
    item_slug = list_cafes[0]["menu_items"][0]["slug"]
    response = client.delete(f"/api/cafes/{cafe_slug}/menu/{item_slug}", headers=headers)
    assert response.status_code == 403

def test_delete_menu_item_not_found1(client, list_cafes, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = "dont exist" # Non-existant slug
    item_slug = list_cafes[0]["menu_items"][0]["slug"]
    response = client.delete(f"/api/cafes/{cafe_slug}/menu/{item_slug}", headers=headers)
    assert response.status_code == 404

def test_delete_menu_item_not_found2(client, list_cafes, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = list_cafes[0]["slug"]
    item_slug = "dont exist" # Non-existant slug
    response = client.delete(f"/api/cafes/{cafe_slug}/menu/{item_slug}", headers=headers)
    assert response.status_code == 404

# --------------------------------------
#       /api/cafes/{cafe_slug}/staff
# --------------------------------------

def test_list_staff_success(client, list_cafes):
    cafe_slug = list_cafes[0]["slug"]
    response = client.get(f"/api/cafes/{cafe_slug}/staff")
    assert response.status_code == 200

def test_create_staff_member_success(client, list_cafes, auth_login):
    cafe_slug = list_cafes[0]["slug"]
    staff_data = {
        "username": "TestStaff",
        "role": "Bénévole"
    }
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    response = client.post(f"/api/cafes/{cafe_slug}/staff", json=staff_data, headers=headers)
    assert response.status_code == 200

def test_create_staff_member_unauthorized(client, list_cafes):
    cafe_slug = list_cafes[0]["slug"]
    staff_data = {
        "username": "TestStaff",
        "role": "Bénévole"
    }
    response = client.post(f"/api/cafes/{cafe_slug}/staff", json=staff_data)
    assert response.status_code == 401

def test_create_staff_member_forbidden(client, list_cafes):
    cafe_slug = list_cafes[1]["slug"]
    staff_data = {
        "username": "TestStaff",
        "role": "Bénévole"
    }
    response = client.post(f"/api/cafes/{cafe_slug}/staff", json=staff_data)
    assert response.status_code == 401

def test_create_staff_member_conflict(client, list_cafes, auth_login):
    cafe_slug = list_cafes[0]["slug"]
    staff_data = {
        "username": "TestStaff",
        "role": "Bénévole"
    }
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    response = client.post(f"/api/cafes/{cafe_slug}/staff", json=staff_data, headers=headers)
    assert response.status_code == 409

# --------------------------------------
#       /api/cafes/{cafe_slug}/staff{username}
# --------------------------------------

def test_update_staff_member_success(client, list_cafes, auth_login):
    cafe_slug = list_cafes[0]["slug"]
    username = "TestStaff"
    staff_data = {
        "role": "Admin"
    }
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    response = client.put(f"/api/cafes/{cafe_slug}/staff/{username}", json=staff_data, headers=headers)
    assert response.status_code == 200

def test_update_staff_member_unauthorized(client, list_cafes):
    cafe_slug = list_cafes[0]["slug"]
    username = "TestStaff"
    staff_data = {
        "role": "Admin"
    }

    response = client.put(f"/api/cafes/{cafe_slug}/staff/{username}", json=staff_data)
    assert response.status_code == 401

def test_update_staff_member_forbidden(client, list_cafes, auth_login):
    cafe_slug = list_cafes[1]["slug"]
    username = "TestStaff"
    staff_data = {
        "role": "Admin"
    }
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    response = client.put(f"/api/cafes/{cafe_slug}/staff/{username}", json=staff_data, headers=headers)
    assert response.status_code == 403

def test_update_staff_member_not_found1(client, list_cafes, auth_login):
    cafe_slug = "dont exist"
    username = "TestStaff"
    staff_data = {
        "role": "Admin"
    }
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    response = client.put(f"/api/cafes/{cafe_slug}/staff/{username}", json=staff_data, headers=headers)
    assert response.status_code == 404

def test_update_staff_member_not_found2(client, list_cafes, auth_login):
    cafe_slug = list_cafes[0]["slug"]
    username = "dont exist"
    staff_data = {
        "role": "Admin"
    }
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    response = client.put(f"/api/cafes/{cafe_slug}/staff/{username}", json=staff_data, headers=headers)
    assert response.status_code == 404

def test_delete_staff_member_success(client, list_cafes, auth_login):
    cafe_slug = list_cafes[0]["slug"]
    username = "TestStaff"
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    response = client.delete(f"/api/cafes/{cafe_slug}/staff/{username}", headers=headers)
    assert response.status_code == 200

def test_delete_staff_member_unauthorized(client, list_cafes):
    cafe_slug = list_cafes[0]["slug"]
    username = "TestStaff"
    response = client.delete(f"/api/cafes/{cafe_slug}/staff/{username}")
    assert response.status_code == 401

def test_delete_staff_member_forbidden(client, list_cafes, auth_login):
    cafe_slug = list_cafes[1]["slug"]
    username = "TestStaff"
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    response = client.delete(f"/api/cafes/{cafe_slug}/staff/{username}", headers=headers)
    assert response.status_code == 403

def test_delete_staff_member_not_found1(client, list_cafes, auth_login):
    cafe_slug = "dont exist" # Non-existant slug
    username = "TestStaff"
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    response = client.delete(f"/api/cafes/{cafe_slug}/staff/{username}", headers=headers)
    assert response.status_code == 404

def test_delete_staff_member_not_found2(client, list_cafes, auth_login):
    cafe_slug = list_cafes[0]["slug"]
    username = "dont exist" # Non-existant slug
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    response = client.delete(f"/api/cafes/{cafe_slug}/staff/{username}", headers=headers)
    assert response.status_code == 404

# --------------------------------------
#       /api/cafes/{cafe_slug}/sales-report
# --------------------------------------

def test_get_sales_report_success(client, list_cafes, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = list_cafes[0]["slug"]
    response = client.get(f"/api/cafes/{cafe_slug}/sales-report", headers=headers)
    assert response.status_code == 200

def test_get_sales_report_unauthorized(client, list_cafes):
    cafe_slug = list_cafes[0]["slug"]
    response = client.get(f"/api/cafes/{cafe_slug}/sales-report")
    assert response.status_code == 401

def test_get_sales_report_forbidden(client, list_cafes, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = list_cafes[1]["slug"]
    response = client.get(f"/api/cafes/{cafe_slug}/sales-report", headers=headers)
    assert response.status_code == 403

def test_get_sales_report_not_found(client, auth_login):
    tokens = auth_login
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}"
    }
    cafe_slug = "dont-exist"  # Non-existent slug
    response = client.get(f"/api/cafes/{cafe_slug}/sales-report", headers=headers)
    assert response.status_code == 404

# -----------------------------
#       /api/search
# -----------------------------

def test_search(client):
    response = client.get("/api/search?query=cafe&sort=name")
    assert response.status_code == 200
