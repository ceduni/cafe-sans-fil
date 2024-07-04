import unittest
from unittest.mock import patch
from recommender_systems.systems.items_recommenders.health_bot import *

'''
Note: The order of application of the @patch decorators (bottom to top) corresponds to the order
in which the mocked objects are passed as arguments to the test method, from left to right.
'''

class TestHealthBot(unittest.TestCase):

    @patch('recommender_systems.utils.utilitaries.health_score')
    def test_sort_by_health_score(self, mock_health_score):
        items = [
            {'slug': 'item1', 'health_score': -6},
            {'slug': 'item2'},
            {'slug': 'item3', 'health_score': 4}
        ]

        mock_health_score.return_value = 10

        self.assertEqual(sort_by_health_score(items), ['item1', 'item3', 'item2'])


    @patch('recommender_systems.utils.db_utils.get_cafe_items')
    @patch('recommender_systems.systems.items_recommenders.health_bot.sort_by_health_score')
    def test_main(self, mock_sort_by_health_score, mock_get_cafe_items):
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

        mock_get_cafe_items.side_effect = [items_1, items_2, items_3]

        mock_sort_by_health_score.side_effect = [
            ['item1', 'item3', 'item2'],
            ['item5', 'item6', 'item4'],
            ['item9', 'item8', 'item7']
        ]

        result = {
            'cafe1': ['item1', 'item3', 'item2'],
            'cafe2': ['item5', 'item6', 'item4'],
            'cafe3': ['item9', 'item8', 'item7']
        }

        self.assertEqual(main(cafe_list), result)
        

if __name__ == '__main__':
    unittest.main()