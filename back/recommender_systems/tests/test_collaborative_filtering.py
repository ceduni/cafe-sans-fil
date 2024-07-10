import unittest
from unittest.mock import patch
from typing import List
from recommender_systems.systems.items_recommenders.collaborative_filtering import *

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

class TestCollaborativeFiltering(unittest.TestCase):
    def setUp(self):
        self.user = {'user_id':'user1', 'username':'username1'}
        self.users = [
            {'user_id':'user2', 'username':'username2'},
            {'user_id':'user3', 'username':'username3'}
        ]
        self.orders = [
            ({'cafe_slug': 'cafe1', 'items': [{'item_slug':'item1'}, {'item_slug':'item2'}, {'item_slug':'item3'}]}, 200),
            ({'cafe_slug': 'cafe2', 'items': [{'item_slug':'item1'}, {'item_slug':'item2'}, {'item_slug':'item7'}, {'item_slug':'item8'}, {'item_slug':'item6'}]}, 200),
            ({'cafe_slug': 'cafe3', 'items': [{'item_slug':'item1'}, {'item_slug':'item2'}, {'item_slug':'item3'}, {'item_slug':'item8'}]}, 200),
        ]
        self.items = [
            {'slug': 'item1', 'likes': ['username1', 'username2', 'username3']},
            {'slug': 'item2', 'likes': ['username1', 'username3']},
            {'slug': 'item3', 'likes': []},
            {'slug': 'item4', 'likes': ['username3']},
            {'slug': 'item5', 'likes': ['username1', 'username3']},
            {'slug': 'item6', 'likes': []},
            {'slug': 'item7', 'likes': ['username2']},
            {'slug': 'item8', 'likes': ['username2', 'username3']},
        ]

    def test_main_no_user(self):
        with self.assertRaises(ValueError):
            main(self.users, None)

    @patch('recommender_systems.utils.db_utils.get_all_items')
    @patch('recommender_systems.utils.db_utils.get_all_user_likes')
    def test_main_no_other_users(self, mock_get_user_likes, mock_get_all_items):
        mock_get_user_likes.return_value = ['item1', 'item2']
        mock_get_all_items.return_value = [
            ({'slug': 'item1'}, 200),
            ({'slug': 'item2'}, 200)
        ]
        result = main([], self.user)
        self.assertEqual(result, ['item1', 'item2'])

    @patch('recommender_systems.utils.api_calls.OrderApi.get_user_orders')
    @patch('recommender_systems.utils.db_utils.get_all_items')
    @patch('recommender_systems.utils.api_calls.OrderApi.get_order')
    def test_main_with_other_users(self, mock_api_get_order,  mock_get_all_items, mock_api_get_user_orders):
        
        mock_api_get_user_orders.side_effect = lambda auth_token, username, params: manage_user_orders(auth_token=auth_token, username=username, params=params)
        mock_get_all_items.return_value = self.items
        mock_api_get_order.side_effect = self.orders

        result = main(self.users, self.user)
        self.assertCountEqual(result, ['item4', 'item8'])

    @patch('recommender_systems.utils.api_calls.OrderApi.get_user_orders')
    @patch('recommender_systems.utils.db_utils.get_all_items')
    @patch('recommender_systems.utils.api_calls.OrderApi.get_order')
    def test_main_with_other_users_with_similarity_threshold(self, mock_api_get_order,  mock_get_all_items, mock_api_get_user_orders):

        mock_api_get_user_orders.side_effect = lambda auth_token, username, params: manage_user_orders(auth_token=auth_token, username=username, params=params)
        mock_get_all_items.return_value = self.items
        mock_api_get_order.side_effect = self.orders

        result = main(self.users, self.user, similarity_threshold=2.7)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()