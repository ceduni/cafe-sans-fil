from recommender_systems.systems.items_recommenders.knowledge_based import *

def test_allergenic_foods():
    user_allergens = {
        "soy": 1,
        "lactose": 3
    }

    menu_items = [
        {
            "slug": "test",
            "allergens": ["soy", "lactose"]
        },
        {
            "slug": "test2",
            "allergens": []
        },
        {
            "slug": "test3",
            "allergens": ["fish", "gluten"]
        },
        {
            "slug": "test4",
            "allergens": ["lactose", "nuts"]
        }
    ]

    assert allergenic_foods(user_allergens, menu_items) == ["test", "test4"]

def test_diet_category_cluster():
    items = [
        {
            "slug": "test",
            "diets": ["gluten-free", "vegetarian", "nut-free"],
            "category": "A"
        },
        {
            "slug": "test2",
            "diets": [],
            "category": "C"
        },
        {
            "slug": "test3",
            "diets": ["vegetarian", "vegan"],
            "category": "A"
        },
        {
            "slug": "test4",
            "diets": ["dairy-free", "nut-free"],
            "category": "B"
        }
    ]

    assert diet_category_cluster(items) == {
        "gluten-free": {
            "A": ["test"]
        },
        "vegetarian": {
            "A": ["test", "test3"]
        },
        "vegan": {
            "A": ["test3"]
        },
        "dairy-free": {
            "B": ["test4"]
        },
        "nut-free": {
            "A": ["test"],
            "B": ["test4"]
        },
        "no_diet": {
            "C": ["test2"]
        }
    }

def test_main():
    actual_cafe = {
        "slug": "cafe1",
        "menu_items": [
            {
                "slug": "test",
                "diets": ["gluten-free", "vegetarian", "nut-free"],
                "category": "A",
                "allergens": ["soy", "lactose"]            
            },
            {
                "slug": "test2",
                "diets": [],
                "category": "C",
                "allergens": ["lactose", "nuts"]
            },
            {
                "slug": "test3",
                "diets": ["vegetarian", "vegan"],
                "category": "A",
                "allergens": ["fish", "gluten"]
            },
            {
                "slug": "test4",
                "diets": ["dairy-free", "nut-free"],
                "category": "B",
                "allergens": []
            }
        ]
    }

    user = {
        "diet_profile": {
            "allergens": {
                "soy": 1,
                "lactose": 3
            },
            "diets": ["gluten-free", "vegetarian", "nut-free"],
            "food_categories": ["B"]
        }
    }

    user_2 = {
        "diet_profile": {
            "allergens": {
                "soy": 3,
                "gluten": 3
            },
            "diets": [],
            "food_categories": ["C"]
        }
    }

    user_3 = {
        "diet_profile": {
            "allergens": {},
            "diets": ["vegetarian"],
            "food_categories": []
        }
    }

    user_4 = {
        "diet_profile": {
            "allergens": {},
            "diets": [],
            "food_categories": []
        }
    }

    assert main(actual_cafe, user) == ["test4"]
    assert main(actual_cafe, user_2) == ["test2"]
    assert sorted(main(actual_cafe, user_3), reverse=False) == ["test", "test3"]
    assert sorted(main(actual_cafe, user_4), reverse=False) == ['test', 'test2', 'test3', 'test4']



if __name__ == "__main__":
    print("Running tests...")
    test_allergenic_foods()
    test_diet_category_cluster()
    test_main()
    print("All tests passed!")