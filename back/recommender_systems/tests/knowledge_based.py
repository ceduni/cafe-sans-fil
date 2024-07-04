from recommender_systems.systems.items_recommenders.knowledge_based import *
import unittest

# Assuming the functions allergenic_foods, diet_category_cluster, and main are defined elsewhere
# from your_module import allergenic_foods, diet_category_cluster, main

class TestKnowledgeBased(unittest.TestCase):

    def test_allergenic_foods(self):
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

        self.assertEqual(allergenic_foods(user_allergens, menu_items), ["test", "test4"])

    def test_diet_category_cluster(self):
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

        expected_result = {
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

        self.assertEqual(diet_category_cluster(items), expected_result)

    def test_main(self):
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

        self.assertEqual(main(actual_cafe, user), ["test4"])
        self.assertEqual(main(actual_cafe, user_2), ["test2"])
        self.assertEqual(sorted(main(actual_cafe, user_3)), ["test", "test3"])
        self.assertEqual(sorted(main(actual_cafe, user_4)), ['test', 'test2', 'test3', 'test4'])

if __name__ == "__main__":
    unittest.main()
