import unittest
from unittest.mock import MagicMock
from app.models.cafe_model import MenuItem
from recommender_systems.routines.clustering import numeric_foods, create_clusters

class TestClustering(unittest.TestCase):
    def test_numeric_foods(self):
        items = [
            {
                "nutritional_informations": {
                    "calories": 100,
                    "lipid": 10,
                    "protein": 10,
                    "carbohydrates": 10,
                    "sugar": 10,
                    "sodium": 10,
                    "fiber": 10,
                    "vitamins": 10,
                    "saturated_fat": 10,
                    "percentage_fruit_vegetables_nuts": 10
                }
            },
            {
                "nutritional_informations": {
                    "calories": 1000,
                    "lipid": None,
                    "protein": 30,
                    "carbohydrates": None,
                    "sugar": 10,
                    "sodium": 10,
                    "fiber": 2,
                    "vitamins": 10,
                    "saturated_fat": 10,
                    "percentage_fruit_vegetables_nuts": None
                }
            }
        ]
        data = numeric_foods(items)
        expected = [[100, 10, 10, 10, 10, 10, 10, 10, 10, 10], [1000, 0, 30, 0, 10, 10, 2, 10, 10, 0]]
        self.assertEqual(data, expected)

    def test_create_clusters(self):
        labels = [0, 0, 1, 1]
        items = ['item1', 'item2', 'item3', 'item4']
        clusters = create_clusters(labels, items)
        self.assertRaises(ValueError, lambda : create_clusters([], []))
        self.assertRaises(ValueError, lambda : create_clusters(labels, []))
        self.assertEqual(create_clusters([], items)['0'], items)
        self.assertCountEqual(clusters["0"], [items[0], items[1]])
        self.assertCountEqual(clusters["1"], [items[2], items[3]])

if __name__ == '__main__':
    unittest.main()