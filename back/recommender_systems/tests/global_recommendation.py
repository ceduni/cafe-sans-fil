from app.models.cafe_model import Cafe, MenuItem
import recommender_systems.systems.global_recommendation as GR
import pytest

@pytest.fixture(scope="module")
def generate_cafe() -> Cafe:
    items = [
        {
            "name": "Orange",
            "tags": ["orange"],
            "description": "orange",
            "price": 1.3,
            "options": [],
            "diets": [""],
            "category": "Fruit",
            "allergens": [],
            "likes": ["a", "b", "c", "d"],
        },
        {
            "name": "Vegan sandwich",
            "tags": ["Vegan sandwich"],
            "description": "Vegan sandwich",
            "price": 7,
            "options": [],
            "diets": ["vegan"],
            "category": "Sandwich",
            "allergens": ["soy", "sesame"],
            "likes": ["e", "b", "g", "z", "k"],
        },
        {
            "name": "Vegetalian wrap",
            "tags": ["Vegetalian wrap"],
            "description": "Vegetalian wrap",
            "price": 10.6,
            "options": [],
            "diets": ["Vegetalian"],
            "category": "wrap",
            "allergens": ["peanut", "celery", "lupin"],
            "likes": [],
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
    return cafe

def test_main(cafe: Cafe):
    assert GR.main(cafe)[0].name == "Vegan sandwich"



if __name__ == "__main__":
    generate_cafe()
    test_main()