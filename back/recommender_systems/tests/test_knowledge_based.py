from recommender_systems.systems.items_recommenders.knowledge_based import *
import unittest
from unittest.mock import patch

# Assuming the functions allergenic_foods, diet_category_cluster, and main are defined elsewhere
# from your_module import allergenic_foods, diet_category_cluster, main

'''
Note: The order of application of the @patch decorators (bottom to top) corresponds to the order
in which the mocked objects are passed as arguments to the test method, from left to right.
'''

class TestKnowledgeBased(unittest.TestCase):
    def setUp(self) -> None:
        self.user_2 = {
            "diet_profile": {
                "allergens": {
                    "soy": 3,
                    "gluten": 3
                },
                "diets": [],
                "prefered_nutrients": {}    
            }
        }

        self.user_3 = {
            "diet_profile": {
                "allergens": {},
                "diets": [
                    {
                        "name": "vegetarian",
                        "description": "Vegetarian",
                        "forbidden_foods": ["viande", "lait", "oeuf", "poisson"]
                    }
                ],
                "prefered_nutrients": {},
            }
        }

        self.user_4 = {
            "diet_profile": {
                "allergens": {},
                "diets": [
                    {
                        "name": "vegetarian",
                        "description": "Vegetarian",
                        "forbidden_foods": ["viande", "lait", "oeuf", "poisson"]
                    }
                ],
                "prefered_nutrients": {
                    "protein": 3,
                    "fiber": 3
                },
            }
        }

        self.diet = {
            "name": "gluten-free",
            "description": "Gluten-free",
            "forbidden_foods": ["tomate", "miel", "poisson"]
        }

        self.diet_2 = {
            "name": "vegetarian",
            "description": "Vegetarian",
            "forbidden_foods": ["viande", "lait", "oeuf", "poisson"]
        }

        self.diet_3 = {
            "name": "nut-free",
            "description": "Nut-free",
            "forbidden_foods": ["porc", "ble", "alcool", "beurre"]
        }

        self.item = {
            "slug": "test",
            "ingredients": ["viande", "lait"],
        }

        self.item_2 = {
            "slug": "test2",
            "ingredients": ["alcool", "porc"],
        }

        self.allergens = {
            "soja": 1,
            "lait": 1,
            "viande": 1,
            "alcool": 3
        }

    def test_regroup_by_diet(self):
        result = regroup_by_diet([self.item, self.item_2], [self.diet, self.diet_2, self.diet_3])
        excepted = {
            "gluten-free": [self.item, self.item_2],
            "vegetarian": [self.item_2],
            "nut-free": [self.item]
        }
        self.assertEqual(result, excepted)
        
    def test_remove_allergenic_items(self):
        result = remove_allergenic_items([self.item, self.item_2], self.allergens)
        excepted = ['test']
        self.assertEqual(result, excepted)
        self.assertEqual(remove_allergenic_items([], self.allergens), [])
        self.assertEqual(remove_allergenic_items([self.item, self.item_2], {}), ['test', 'test2'])
        self.assertEqual(remove_allergenic_items([], {}), [])

class TestMain(unittest.TestCase):

    def setUp(self) -> None:
        self.user_1 = {
            "diet_profile": {
                "allergens": {
                    "soja": 1,
                    "lait": 3
                },
                "diets": [
                    {
                        "name": "gluten-free",
                        "description": "Gluten-free",
                        "forbidden_foods": ["lait", "oeuf", "poisson", "viande"]
                    },
                    {
                        "name": "vegetarian",
                        "description": "Vegetarian",
                        "forbidden_foods": ["viande", "lait", "oeuf", "poisson"]
                    },
                    {
                        "name": "nut-free",
                        "description": "Nut-free",
                        "forbidden_foods": ["viande", "sucre", "alcool", "beurre"]
                    }
                ],
                "prefered_nutrients": {
                    "vitaminA": 2,
                    "vitaminC": 3
                },
            }
        }

        self.user_2 = {
            "diet_profile": {
                "allergens": {
                    "soja": 1,
                    "lait": 3
                },
                "diets": [],
                "prefered_nutrients": {},
            }
        }

        self.user_3 = {
            "diet_profile": {
                "allergens": {
                    "soja": 1,
                    "ble": 3
                },
                "diets": [],
                "prefered_nutrients": {
                    "vitaminA": 2,
                    "vitaminC": 3
                },
            }
        }
        
        self.user_4 = {
            "diet_profile": {
                "allergens": {
                    "soja": 1,
                    "ble": 3
                },
                "diets": [
                    {
                        "name": "gluten-free",
                        "description": "Gluten-free",
                        "forbidden_foods": ["lait", "oeuf", "poisson", "viande"]
                    },
                    {
                        "name": "vegetarian",
                        "description": "Vegetarian",
                        "forbidden_foods": ["viande", "lait", "oeuf", "poisson"]
                    },
                    {
                        "name": "nut-free",
                        "description": "Nut-free",
                        "forbidden_foods": ["viande", "sucre", "alcool", "beurre"]
                    }
                ],
                "prefered_nutrients": {},
            }
        }

        self.item_1 = {
            "slug": "item1",
            "ingredients": ["viande", "lait"],
            'nutritional_informations': {
                'vitaminA': 0.85, 
                'carbhydrates': 0, 
                'vitaminC': 120
            },
        }

        self.item_2 = {
            "slug": "item2",
            "ingredients": ["ble", "porc"],
                'nutritional_informations': {
                'vitaminA': 0.9, 
                'carbhydrates': 0, 
                'vitaminC': 40
            },
        }

        self.item_3 = {
            "slug": "item3",
            "ingredients": ["noix", "fraises"],
            'nutritional_informations': {
                'vitaminA': 0.3, 
                'carbhydrates': 0, 
                'vitaminC': 20
            },
        }

        self.item_4 = {
            "slug": "item4",
            "ingredients": ["noix", "fraises"],
            'nutritional_informations': {
                'vitaminA': 0.9, 
                'carbhydrates': 5, 
                'vitaminC': 130
            },
        }

        self.actual_cafe = {
            "menu_items": [self.item_1, self.item_2, self.item_3],
        }

        self.actual_cafe_2 = {
            "menu_items": [self.item_1, self.item_2, self.item_3, self.item_4],
        }

    def test_invalid_actual_cafe_type(self):
        with self.assertRaises(TypeError):
            main("not_a_dict", self.user_1)

    def test_invalid_user_type(self):
        with self.assertRaises(TypeError):
            main(self.actual_cafe, "not_a_dict")

    def test_missing_menu_items_key(self):
        invalid_cafe = {'no_menu_items_key': []}
        with self.assertRaises(KeyError):
            main(invalid_cafe, self.user_1)

    def test_missing_diet_profile_key(self):
        invalid_user = {'no_diet_profile_key': []}
        with self.assertRaises(KeyError):
            main(self.actual_cafe, invalid_user)

    def test_no_diets_no_nutrients(self):
        expected = ['item2', 'item3']
        result = main(self.actual_cafe, self.user_2)
        self.assertCountEqual(result, expected)

    def test_only_nutrients(self):
        expected = ['item1']
        result = main(self.actual_cafe, self.user_3)
        self.assertCountEqual(result, expected)

    def test_only_diet(self):
        expected = ['item3']
        result = main(self.actual_cafe, self.user_4)
        self.assertCountEqual(result, expected)

    def test_diet_and_nutrients(self):
        expected_1 = []
        result_1 = main(self.actual_cafe, self.user_1)
        self.assertCountEqual(result_1, expected_1)

        expected_2 = ['item4']
        result_2 = main(self.actual_cafe_2, self.user_1)
        self.assertCountEqual(result_2, expected_2)


if __name__ == "__main__":
    unittest.main()
