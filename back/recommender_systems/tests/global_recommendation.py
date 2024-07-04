from recommender_systems.systems.items_recommenders.global_recommendation import *
import unittest
from unittest.mock import patch, MagicMock

class TestMain(unittest.TestCase):

    @patch('recommender_systems.utils.db_utils.get_cafe_items')
    @patch('recommender_systems.utils.db_utils.get_all_orders')
    @patch('recommender_systems.utils.utilitaries.most_bought_items')
    @patch('recommender_systems.utils.utilitaries.most_liked_items')
    @patch('recommender_systems.utils.db_utils.get_item')
    def test_main(self, mock_get_item, mock_most_liked_items, mock_most_bought_items, mock_get_all_orders, mock_get_cafe_items):
        # Test case: Empty cafe items
        mock_get_cafe_items.return_value = []
        mock_most_bought_items.return_value = []
        result = main(MagicMock(slug='test_cafe'))
        self.assertEqual(result, [])

        # Test case: More than 50 cafe items
        mock_get_cafe_items.return_value = [MagicMock(slug='item1'), MagicMock(slug='item2'), MagicMock(slug='item3')]
        mock_most_bought_items.return_value = ['item1', 'item2', 'item3']
        mock_most_liked_items.return_value = ['item1', 'item2']
        mock_get_all_orders.return_value = [MagicMock(id='order1'), MagicMock(id='order2'), MagicMock(id='order3')]
        mock_get_item.side_effect = lambda cafe_slug, item_slug: MagicMock(slug=item_slug)
        result = main(MagicMock(slug='test_cafe'))
        self.assertEqual(result, ['item1', 'item2'])

        # Test case: Less than or equal to 50 cafe items
        mock_get_cafe_items.return_value = [MagicMock(slug='item1'), MagicMock(slug='item2')]
        mock_most_bought_items.return_value = ['item1', 'item2', 'item3']
        mock_most_liked_items.return_value = ['item1', 'item2']
        mock_get_all_orders.return_value = [MagicMock(slug='order1'), MagicMock(slug='order2'), MagicMock(slug='order3')]
        mock_get_item.side_effect = lambda cafe_slug, item_slug: MagicMock(slug=item_slug)
        result = main(MagicMock(slug='test_cafe'))
        self.assertEqual(result, ['item1', 'item2'])

if __name__ == '__main__':
    unittest.main()