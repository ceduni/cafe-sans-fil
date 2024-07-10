from recommender_systems.systems.items_recommenders.global_recommendation import *
import unittest
from unittest.mock import patch, MagicMock

'''
Note: The order of application of the @patch decorators (bottom to top) corresponds to the order
in which the mocked objects are passed as arguments to the test method, from left to right.
'''

def manage_get_item(slug: str) -> MenuItem:
    match slug:
        case 'item1':
            return {'slug': 'item1', 'likes': ['user1']}
        case 'item2':
            return {'slug': 'item2', 'likes': ['user1', 'user3', 'user4']}
        case 'item3':
            return {'slug': 'item3', 'likes': ['user1', 'user4']}
        case 'item4':
            return {'slug': 'item4', 'likes': ['user2', 'user3', 'user4', 'user5']}
        case 'item5':
            return {'slug': 'item5', 'likes': []}
        case 'item6':
            return {'slug': 'item6', 'likes': ['user7', 'user8']}
        

class TestGlobalRecommendation(unittest.TestCase):

    @patch('recommender_systems.utils.db_utils.get_cafe_items')
    def test_main_1(self, mock_get_cafe_items):
        # Test1 Empty cafe
        mock_get_cafe_items.return_value = []
        result = main({'slug': 'test_cafe'})
        self.assertEqual(result, [])

    @patch('recommender_systems.utils.db_utils.get_cafe_items')
    @patch('recommender_systems.utils.db_utils.get_all_orders')
    @patch('recommender_systems.utils.db_utils.get_item')
    def test_main_2(self, mock_get_item, mock_get_all_orders, mock_get_cafe_items):
        # Test2: Not empty cafe
        mock_get_cafe_items.return_value = [
            {'slug': 'item1'}, 
            {'slug': 'item2'}, 
            {'slug': 'item3'},
        ]
        mock_get_all_orders.return_value = [
            {'order_id': 'order1', 'items': [{'item_slug': 'item1'}, {'item_slug': 'item2'}]},
            {'order_id': 'order2', 'items': [{'item_slug': 'item3'}, {'item_slug': 'item4'}]},
            {'order_id': 'order3', 'items': [{'item_slug': 'item5'}, {'item_slug': 'item6'}]},
        ]
        mock_get_item.side_effect = lambda cafe_slug, item_slug: manage_get_item(item_slug)
        result = main({'slug': 'test_cafe'})
        self.assertCountEqual(result, ['item4', 'item2', 'item6'])

if __name__ == '__main__':
    unittest.main()