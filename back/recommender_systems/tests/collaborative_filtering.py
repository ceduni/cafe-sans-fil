import unittest
from unittest.mock import patch
from typing import List
from recommender_systems.systems.items_recommenders.collaborative_filtering import *

'''
Note: The order of application of the @patch decorators (bottom to top) corresponds to the order
in which the mocked objects are passed as arguments to the test method, from left to right.
'''

class TestCollaborativeFiltering(unittest.TestCase):
    def setUp(self):
        self.user = {'id':'user1', 'username':'username1'}
        self.users = [
            {'id':'user2', 'username':'username2'},
            {'id':'user3', 'username':'username3'}
        ]

    def test_main_no_user(self):
        with self.assertRaises(ValueError):
            main(self.users, None)

    @patch('recommender_systems.utils.db_utils.get_user_likes')
    def test_main_no_other_users(self, mock_get_user_likes):
        mock_get_user_likes.return_value = ['item1', 'item2']
        
        result = main([], self.user)
        self.assertEqual(result, ['item1', 'item2'])

    @patch('recommender_systems.utils.db_utils.get_user_visited_cafe')
    @patch('recommender_systems.utils.db_utils.get_user_likes')
    @patch('recommender_systems.utils.db_utils.get_user_orders')
    @patch('recommender_systems.utils.utilitaries.users_similarity')
    @patch('recommender_systems.utils.utilitaries.list_items')
    def test_main_with_other_users(self, mock_list_items, mock_users_similarity, mock_get_user_orders, mock_get_user_likes, mock_get_user_visited_cafe):
        mock_get_user_visited_cafe.side_effect = [
            ['cafe1', 'cafe2'],
            ['cafe1', 'cafe3'],
            ['cafe4']
        ]
        mock_get_user_likes.side_effect = [
            ['item1', 'item2'],
            ['item1', 'item2', 'item6'],
            ['item4']
        ]
        mock_get_user_orders.side_effect = [
            ['order2'],
            ['order2'],
            ['order3']
        ]
        mock_list_items.side_effect = [
            ['item1', 'item2', 'item3'],
            ['item4', 'item3', 'item6'],
            ['item4', 'item8']
        ]
        mock_users_similarity.side_effect = [1.99, 0]  # Similarities between User1 and other users

        result = main(self.users, self.user)
        
        # Expected: recommendations based on user similarity
        self.assertTrue(any(item in result for item in ['item4', 'item6']))


if __name__ == '__main__':
    unittest.main()