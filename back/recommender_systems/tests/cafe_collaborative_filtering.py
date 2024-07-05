import unittest
from unittest.mock import patch, MagicMock

from recommender_systems.systems.cafe_recommenders.collaborative import *

'''
Note: The order of application of the @patch decorators (bottom to top) corresponds to the order
in which the mocked objects are passed as arguments to the test method, from left to right.
'''

#TODO
class TestMainFunction(unittest.TestCase):

    def setUp(self):
        self.user = {'id': 'user1', 'username': 'username1'}
        self.users = [
            {'id': 'user2', 'username': 'username2'},
            {'id': 'user3', 'username': 'username3'},
        ]

    def test_main_no_user(self):
        with self.assertRaises(ValueError):
            main(self.users, None)

    @patch('recommender_systems.utils.db_utils.get_user_visited_cafe')
    def test_main_no_other_users(self, mock_get_user_visited_cafe):
        mock_get_user_visited_cafe.return_value = ['cafe1', 'cafe2']
        
        result = main([], self.user)
        self.assertEqual(result, ['cafe1', 'cafe2'])

    @patch('recommender_systems.utils.db_utils.get_user_visited_cafe')
    @patch('recommender_systems.utils.db_utils.get_user_likes')
    @patch('recommender_systems.utils.db_utils.get_user_orders')
    @patch('recommender_systems.utils.utilitaries.users_similarity')
    def test_main_with_other_users(self, mock_users_similarity, mock_get_user_orders, mock_get_user_likes, mock_get_user_visited_cafe):
        mock_get_user_visited_cafe.side_effect = [
            ['cafe1', 'cafe2'],
            ['cafe3'],
            ['cafe4'],
            ['cafe3'],
            ['cafe4']         
        ]
        mock_get_user_likes.side_effect = [
            ['item1', 'item2'],
            ['item3'],
            ['item4']
        ]
        mock_get_user_orders.side_effect = [
            ['order1'],
            ['order2'],
            ['order3']
        ]
        mock_users_similarity.side_effect = [0.9, 0.8]  # Similarities between User1 and other users

        result = main(self.users, self.user)
        
        self.assertIn('cafe3', result)
        self.assertIn('cafe4', result)
        self.assertNotIn('cafe1', result)
        self.assertNotIn('cafe2', result)

if __name__ == '__main__':
    unittest.main()