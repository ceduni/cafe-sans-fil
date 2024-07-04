from recommender_systems.systems.items_recommenders.global_recommendation import *
import unittest
from unittest.mock import patch, MagicMock

'''
Note: The order of application of the @patch decorators (bottom to top) corresponds to the order
in which the mocked objects are passed as arguments to the test method, from left to right.
'''

class TestGlobalRecommendation(unittest.TestCase):

    @patch('recommender_systems.utils.db_utils.get_cafe_items')
    @patch('recommender_systems.utils.db_utils.get_all_orders')
    @patch('recommender_systems.utils.utilitaries.most_bought_items')
    @patch('recommender_systems.utils.utilitaries.most_liked_items')
    @patch('recommender_systems.utils.db_utils.get_item')
    def test_main(self, mock_get_item, mock_most_liked_items, mock_most_bought_items, mock_get_all_orders, mock_get_cafe_items):
        # Test case: Empty cafe items
        mock_get_cafe_items.return_value = []
        mock_most_bought_items.return_value = []
        result = main({'slug': 'test_cafe'})
        self.assertEqual(result, [])

        # Test case: More than 50 cafe items
        mock_get_cafe_items.return_value = [{'slug': 'item1'}, {'slug': 'item2'}, {'slug': 'item3'}]
        mock_most_bought_items.return_value = ['item1', 'item2', 'item3']
        mock_most_liked_items.return_value = ['item1', 'item2']
        mock_get_all_orders.return_value = [{'id': 'order1'}, {'id': 'order2'}, {'id': 'order3'}]
        mock_get_item.side_effect = lambda cafe_slug, item_slug: {'slug': item_slug}
        result = main({'slug': 'test_cafe'})
        self.assertEqual(result, ['item1', 'item2'])

        # Test case: Less than or equal to 50 cafe items
        mock_get_cafe_items.return_value = [{'slug': 'item1'}, {'slug': 'item2'}]
        mock_most_bought_items.return_value = ['item1', 'item2', 'item3']
        mock_most_liked_items.return_value = ['item1', 'item2']
        mock_get_all_orders.return_value = [{'id': 'order1'}, {'id': 'order2'}, {'id': 'order3'}]
        mock_get_item.side_effect = lambda cafe_slug, item_slug: {'slug': item_slug}
        result = main({'slug': 'test_cafe'})
        self.assertEqual(result, ['item1', 'item2'])

if __name__ == '__main__':
    unittest.main()