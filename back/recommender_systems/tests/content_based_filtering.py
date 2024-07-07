from contextlib import AbstractContextManager
from typing import Any
from recommender_systems.systems.items_recommenders.content_based_filtering import *
from unittest.mock import patch, MagicMock
import unittest
import random

'''
Note: The order of application of the @patch decorators (bottom to top) corresponds to the order
in which the mocked objects are passed as arguments to the test method, from left to right.
'''

class TestContentBasedFiltering(unittest.TestCase):

    def setUp(self):
        self.user1 = {'user_id': 'user1', 'username': 'username1'}
        self.cafes = [
            # Cafe1 doesn't contain user2
            {
                'slug': 'cafe1',
                'menu_items': [
                    {'slug': 'item1', 'likes': []}, 
                    {'slug': 'item2', 'likes': ['user1']},
                    {'slug': 'item3', 'likes': ['user5', 'user3']},
                    {'slug': 'item4', 'likes': ['user1', 'user3']},
                    {'slug': 'item5', 'likes': ['user6', 'user3', 'user4']}
                ]
            }, 

            # Cafe2 doesn't contain user1
            {
                'slug': 'cafe2',
                'menu_items': [
                    {'slug': 'item6', 'likes': ['user3', 'user2']}, 
                    {'slug': 'item7', 'likes': ['user7', 'user3', 'user4']},
                    {'slug': 'item8', 'likes': ['user2', 'user3']},
                    {'slug': 'item9', 'likes': ['user2', 'user4', 'user5', 'user6']},
                    {'slug': 'item10', 'likes': []}
                ]
            }
        ]

        self.all_items = ([
            {'slug': 'item1', 'likes': []}, 
            {'slug': 'item2', 'likes': ['user1']},
            {'slug': 'item3', 'likes': ['user2', 'user3']},
            {'slug': 'item4', 'likes': ['user1', 'user3']},
            {'slug': 'item5', 'likes': ['user2', 'user3', 'user4']},
            {'slug': 'item6', 'likes': ['user1', 'user2']}, 
            {'slug': 'item7', 'likes': ['user1', 'user3', 'user4']},
            {'slug': 'item8', 'likes': ['user2', 'user3']},
            {'slug': 'item9', 'likes': ['user1', 'user4', 'user5', 'user6']},
            {'slug': 'item10', 'likes': []}
        ], 200)

    def test_favorite_cluster(self):
        clusters = {
            '0': [
                {'slug': 'a', 'likes': ['1', '2']},
                {'slug': 'b', 'likes': ['3', '1', '6']},
                {'slug': 'c', 'likes': ['3']},
                {'slug': 'd', 'likes': []}
            ],
            '1': [
                {'slug': 'e', 'likes': ['2']},
                {'slug': 'f', 'likes': ['3', '1', '6']},
                {'slug': 'g', 'likes': ['3']},
                {'slug': 'h', 'likes': []}
            ],
            '2': [
                {'slug': 'i', 'likes': ['1', '2', '3']},
                {'slug': 'j', 'likes': ['3', '1', '6']},
                {'slug': 'k', 'likes': ['3', '1']},
                {'slug': 'l', 'likes': ['1']}
            ],
            '3': [
                {'slug': 'm', 'likes': ['2']},
                {'slug': 'n', 'likes': ['6', '1']},
                {'slug': 'o', 'likes': ['3', '1', '6']},
                {'slug': 'p', 'likes': ['5', '1']}
            ],
        }
        user = {
            'user_id': '1'
        }
        
        with self.assertRaises(ValueError):
            favorite_cluster([], user)

        with self.assertRaises(ValueError):
            favorite_cluster(clusters, None)

        with self.assertRaises(ValueError):
            favorite_cluster([], None)

        self.assertEqual(
            favorite_cluster(clusters, user),
            {
                '2': [
                    {'slug': 'i', 'likes': ['1', '2', '3']},
                    {'slug': 'j', 'likes': ['3', '1', '6']},
                    {'slug': 'k', 'likes': ['3', '1']},
                    {'slug': 'l', 'likes': ['1']}
                ],       
            }
        )

    def test_remove_cluster(self):
        clusters = {
            '0': ['a', 'b', 'c'],
            '1': ['d', 'e', 'f'],
            '2': ['g', 'h', 'i'],
            '3': ['j', 'k', 'l'],
            '4': ['m', 'n', 'o'],
        }
        chosen_cluster = {
            '0': ['a', 'b', 'c'],
            '2': ['g', 'h', 'i'],
        }
        
        with self.assertRaises(ValueError):
            remove_cluster(chosen_cluster, {})

        with self.assertRaises(ValueError):
            remove_cluster({}, {})

        self.assertEqual(remove_cluster({}, clusters), clusters)

        self.assertEqual(
            remove_cluster(chosen_cluster, clusters),
            {
                '1': ['d', 'e', 'f'],
                '3': ['j', 'k', 'l'],
                '4': ['m', 'n', 'o'],
            }
        )

    def test_main_1(self):
        # User is None or/and cafe is None.
        self.assertEqual(main(None, None), [])
        self.assertEqual(main(None, {'menu_items': []}), [])
        self.assertEqual(main({'user_id': 'user1'}, None), [])

    # There is no items in the cafe.
    @patch('recommender_systems.utils.db_utils.get_user_likes_in_cafe')
    def test_main_2(self, mock_get_user_likes):
        # No item in the cafe and the user has liked some items.
        mock_get_user_likes.return_value = ['item1', 'item2']
        self.assertEqual(main({'user_id': 'user1'}, {'slug': 'cafe1', 'menu_items': []}), [])

        # No item in the cafe and the user has not liked any item
        mock_get_user_likes.return_value = []
        self.assertEqual(main({'user_id': 'user1'}, {'slug': 'cafe1', 'menu_items': []}), [])

    # # # At least one item in the cafe.
    @patch('recommender_systems.utils.db_utils.get_all_items')
    @patch('recommender_systems.utils.api_calls.CafeApi.get_all_items')
    def test_main_3(self, mock_api_get_all_items, mock_utils_get_all_items):
        # The user has not liked any item
        user = self.user1
        cafe = self.cafes[1]

        mock_api_get_all_items.return_value = ([
            {'slug': 'item6', 'likes': ['user3', 'user2']}, 
            {'slug': 'item7', 'likes': ['user7', 'user3', 'user4']},
            {'slug': 'item8', 'likes': ['user2', 'user3']},
            {'slug': 'item9', 'likes': ['user2', 'user4', 'user5', 'user6']},
            {'slug': 'item10', 'likes': []}
        ], 200)
        
        mock_utils_get_all_items.return_value = self.all_items

        result = main(user, cafe)
        self.assertCountEqual(result, ['item9', 'item7', 'item8', 'item6', 'item10'])

    # # User has bought all items in the cafe.
    @patch('recommender_systems.utils.api_calls.CafeApi.get_all_items')
    @patch('recommender_systems.utils.db_utils.get_user_likes_in_cafe')
    @patch('recommender_systems.utils.utilitaries.items_not_bought_in_cafe')
    def test_main_4(self, mock_items_not_bought_in_cafe, mock_get_user_likes, mock_api_get_all_items):
        user = self.user1
        cafe = self.cafes[0]

        mock_api_get_all_items.return_value = ([
            {'slug': 'item1', 'likes': []}, 
            {'slug': 'item2', 'likes': ['user1']},
            {'slug': 'item3', 'likes': ['user5', 'user3']},
            {'slug': 'item4', 'likes': ['user1', 'user3']},
            {'slug': 'item5', 'likes': ['user6', 'user3', 'user4']}
        ], 200)

        # The user has liked some items.
        mock_items_not_bought_in_cafe.return_value = set()
        mock_get_user_likes.return_value = ['item2', 'item4']
        self.assertCountEqual(main(user, cafe), ['item2', 'item4'])

        # The user has not liked any item.
        mock_get_user_likes.return_value = []
        mock_items_not_bought_in_cafe.return_value = set()
        self.assertCountEqual(main(user, cafe), ['item5', 'item4', 'item3', 'item2', 'item1'])
    
    # At least one item in the cafe and the user has liked some items.
    def test_algorithm(self):
        user = self.user1
        cafe_items = [
            {'slug': 'item1', 'cluster': '0', 'likes': ['user1']}, 
            {'slug': 'item2', 'cluster': '1', 'likes': ['user1']},
            {'slug': 'item3', 'cluster': '2', 'likes': ['user5', 'user3']},
            {'slug': 'item4', 'cluster': '0', 'likes': ['user1', 'user3']},
            {'slug': 'item5', 'cluster': '1', 'likes': ['user6', 'user3', 'user4']}
        ]

        items_not_bought = set([
            'item1', 'item3'
        ])

        self.assertCountEqual(algorithm(user, cafe_items, items_not_bought), ['item1', 'item3'])
        self.assertCountEqual(algorithm(user, cafe_items, items_not_bought, 1), ['item1'])

if __name__ == '__main__':
    unittest.main()