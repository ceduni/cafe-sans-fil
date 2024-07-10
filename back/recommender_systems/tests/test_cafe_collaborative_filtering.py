import unittest
from unittest.mock import patch, MagicMock

from recommender_systems.systems.cafe_recommenders.collaborative import *

'''
Note: The order of application of the @patch decorators (bottom to top) corresponds to the order
in which the mocked objects are passed as arguments to the test method, from left to right.
'''
def manage_user_orders(auth_token, username, params):
    match username:
        case 'username1':
            return ([{'order_id':'order1', 'cafe_slug': 'cafe1'}], 200)
        case 'username2':
            return ([{'order_id':'order2', 'cafe_slug': 'cafe2'}], 200)
        case 'username3':
            return ([{'order_id':'order3', 'cafe_slug': 'cafe3'}], 200)
        case _:
            return ([], 404)
    

class TestMainFunction(unittest.TestCase):

    def setUp(self):
        self.user = {'id': 'user1', 'username': 'username1'}
        self.users = [
            {'id': 'user2', 'username': 'username2'},
            {'id': 'user3', 'username': 'username3'},
        ]
        self.all_items = [
            {'slug': 'item1', 'likes': ['user1', 'user2', 'user3']},
            {'slug': 'item2', 'likes': ['user1', 'user3']},
            {'slug': 'item3', 'likes': []},
            {'slug': 'item4', 'likes': ['user3']},
            {'slug': 'item5', 'likes': ['user1', 'user2']},
            {'slug': 'item6', 'likes': []},
            {'slug': 'item7', 'likes': ['user2']},
            {'slug': 'item8', 'likes': ['user2', 'user3']},
        ]
        self.orders = [
            ({'cafe_slug': 'cafe1', 'items': [{'item_slug':'item1'}, {'item_slug':'item2'}, {'item_slug':'item3'}]}, 200),
            ({'cafe_slug': 'cafe2', 'items': [{'item_slug':'item1'}, {'item_slug':'item2'}, {'item_slug':'item7'}, {'item_slug':'item8'}, {'item_slug':'item6'}]}, 200),
            ({'cafe_slug': 'cafe3', 'items': [{'item_slug':'item1'}, {'item_slug':'item2'}, {'item_slug':'item4'}, {'item_slug':'item8'}]}, 200),
        ]

    def test_main_no_user(self):
        with self.assertRaises(ValueError):
            main(self.users, None)

    @patch('recommender_systems.utils.db_utils.get_user_visited_cafe')
    def test_main_no_other_users(self, mock_get_user_visited_cafe):
        mock_get_user_visited_cafe.return_value = ['cafe1', 'cafe2']
        
        result = main([], self.user)
        self.assertEqual(result, ['cafe1', 'cafe2'])

    @patch('recommender_systems.utils.api_calls.OrderApi.get_user_orders')
    @patch('recommender_systems.utils.db_utils.get_all_items')
    @patch('recommender_systems.utils.api_calls.OrderApi.get_order')
    def test_main_with_other_users(self, mock_api_get_order, mock_get_all_items, mock_api_get_user_orders):
        
        mock_api_get_user_orders.side_effect = lambda auth_token, username, params: manage_user_orders(auth_token=auth_token, username=username, params=params)
        
        mock_get_all_items.return_value = self.all_items

        mock_api_get_order.side_effect = self.orders

        result = main(self.users, self.user)
        self.assertCountEqual(result, ['cafe3', 'cafe2'])

if __name__ == '__main__':
    unittest.main()