import unittest
from unittest.mock import patch, MagicMock

from recommender_systems.systems.cafe_recommenders.collaborative import *

'''
Note: The order of application of the @patch decorators (bottom to top) corresponds to the order
in which the mocked objects are passed as arguments to the test method, from left to right.
'''

#TODO
class TestMainFunction(unittest.TestCase):

    #TODO
    @patch('recommender_systems.utils.db_utils.get_user_visited_cafe')
    @patch('recommender_systems.utils.db_utils.get_user_likes')
    @patch('recommender_systems.utils.db_utils.get_user_orders')
    @patch('recommender_systems.utils.utilitaries.users_similarity')
    def test_main(self, mock_user_visited_cafe, mock_user_likes, mock_user_orders, mock_users_similarity):
        # Test empty users list
        users = []
        user = {'id': 'user1'}
        mock_user_visited_cafe.return_value = []
        self.assertEqual(main(users, user), [])

        # # Test single user in users list
        # users = [MagicMock()]
        # user = MagicMock()
        # self.assertEqual(main(users, user), [])

        # # Test multiple users in users list
        # users = [MagicMock(), MagicMock()]
        # user = MagicMock()
        # self.assertIsInstance(main(users, user), list)

if __name__ == '__main__':
    unittest.main()