import unittest
from unittest.mock import patch
from recommender_systems.systems.items_recommenders.health_bot import *

'''
Note: The order of application of the @patch decorators (bottom to top) corresponds to the order
in which the mocked objects are passed as arguments to the test method, from left to right.
'''

class TestHealthBot(unittest.TestCase):

    def test_sort_by_health_score(self):
        items = [
            {'slug': 'item1', 'health_score': -6},
            {'slug': 'item2', 'nutritional_informations': {
                'calories': 1000,
                'saturated_fat': 20, 
                'sugar': 30,
                'sodium': 10,
                'fiber': None,
                'protein': 6,
                'percentage_fruit_vegetables_nuts': None
            }},
            {'slug': 'item3', 'health_score': 4}
        ]

        self.assertEqual(sort_by_health_score(items), ['item1', 'item3', 'item2'])


    @patch('recommender_systems.utils.api_calls.CafeApi.get_all_items')
    def test_main(self, mock_get_all_items):
        cafe_list = [
            {'slug': 'cafe1'},
            {'slug': 'cafe2'},
            {'slug': 'cafe3'}
        ]

        items_1 = [
            {'slug': 'item1', 'health_score': -6},
            {'slug': 'item2', 'health_score': 10},
            {'slug': 'item3', 'health_score': 4}
        ]

        items_2 = [
            {'slug': 'item4', 'health_score': 14},
            {'slug': 'item5', 'health_score': -7},
            {'slug': 'item6', 'health_score': 4}
        ]

        items_3 = [
            {'slug': 'item7', 'health_score': 20},
            {'slug': 'item8', 'health_score': 0},
            {'slug': 'item9', 'health_score': -8}
        ]

        mock_get_all_items.side_effect = [
            (items_1, 200),
            (items_2, 200),
            (items_3, 200),
        ]

        result = {
            'cafe1': ['item1', 'item3', 'item2'],
            'cafe2': ['item5', 'item6', 'item4'],
            'cafe3': ['item9', 'item8', 'item7']
        }

        self.assertEqual(main(cafe_list), result)
        

if __name__ == '__main__':
    unittest.main()