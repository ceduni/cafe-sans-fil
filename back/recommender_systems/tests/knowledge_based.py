import pytest
from back.app.models.cafe_model import Cafe, MenuItem
from back.app.models.user_model import User, DietProfile


import back.recommender_systems.systems.knowledge_based as KB 

# --------------------------------------
#       Data generation
# --------------------------------------

@pytest.fixture(scope="module")
def generate_user() -> dict:
    pass

@pytest.fixture(scope="module")
def generate_cafe() -> Cafe:
    '''
    items = [
        {
            "name": "Orange",
            "tags": ["orange"],
            "description": "orange",
            "price": 1.3,
            "options": [],
            "diets": [""],
            "category": "Fruit",
            "allergens": []
        },
        {
            "name": "Vegan sandwich",
            "tags": ["Vegan sandwich"],
            "description": "Vegan sandwich",
            "price": 7,
            "options": [],
            "diets": ["vegan"],
            "category": "Sandwich",
            "allergens": ["soy", "sesame"]
        },
    ]
    item_list: list[MenuItem] = []
    for item in items:
        item_list.append(MenuItem(**item))

    data = {
        "name": "Tore et fraction",
        "menu_items": item_list,
    }
    
    cafe = Cafe(**data)
    '''
    pass

def generate_user() -> User:
    #TODO
    pass

# --------------------------------------
#       Tests
# --------------------------------------

def test_allergenic_foods():
    #TODO
    pass

def test_clusters_user_preference():
    #TODO
    pass

def test_main():
    #TODO
    pass