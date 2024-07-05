from contextlib import AbstractContextManager
from typing import Any
from recommender_systems.systems.items_recommenders.content_based_filtering import *
from unittest.mock import patch, MagicMock
import unittest

'''
Note: The order of application of the @patch decorators (bottom to top) corresponds to the order
in which the mocked objects are passed as arguments to the test method, from left to right.
'''

class TestContentBasedFiltering(unittest.TestCase):

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
                {'slug': 'm', 'likes': ['2', '1']},
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
                '3': [
                    {'slug': 'm', 'likes': ['2', '1']},
                    {'slug': 'n', 'likes': ['6', '1']},
                    {'slug': 'o', 'likes': ['3', '1', '6']},
                    {'slug': 'p', 'likes': ['5', '1']}
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

    # # There is no items in the cafe.
    @patch('recommender_systems.utils.db_utils.get_user_likes')
    def test_main_2(self, mock_get_user_likes):
        # No item in the cafe and the user has liked some items.
        mock_get_user_likes.return_value = ['item1', 'item2']
        self.assertEqual(main({'user_id': 'user1'}, {'menu_items': []}), [])

        # No item in the cafe and the user has not liked any item
        mock_get_user_likes.return_value = []
        self.assertEqual(main({'user_id': 'user1'}, {'menu_items': []}), [])

    # # At least one item in the cafe.
    @patch('recommender_systems.utils.utilitaries.most_liked_items')
    @patch('recommender_systems.utils.db_utils.get_user_likes')
    @patch('recommender_systems.utils.utilitaries.meal_not_consumed')
    def test_main_3(self, mock_meal_not_consumed, mock_get_user_likes, mock_most_liked_items):
        # The user has not liked any item
        user = {'user_id': 'user1', 'username': 'username1'}
        cafe = {
            'slug': 'cafe1',
            'menu_items': [{'slug': 'item1'}, 
                {'slug': 'item2','likes': []}
            ]
        }
        mock_get_user_likes.return_value = []
        mock_most_liked_items.return_value = ['item2']
        self.assertEqual(main(user, cafe), ['item2'])

    # # User has bought all items in the cafe.
    @patch('recommender_systems.utils.utilitaries.most_liked_items')
    @patch('recommender_systems.utils.db_utils.get_user_likes')
    @patch('recommender_systems.utils.utilitaries.meal_not_consumed')
    def test_main_4(self, mock_meal_not_consumed, mock_get_user_likes, mock_most_liked_items):
        user = {'user_id': 'user1', 'username': 'username1'}
        cafe = {
            'slug': 'cafe1',
            'menu_items': [
                {
                    'slug': 'item1',
                    'likes': ['user1']
                }, 
                {
                    'slug': 'item2',
                    'likes': []
                }
            ]
        }

        # The user has liked some items.
        mock_meal_not_consumed.return_value = set() 
        mock_get_user_likes.return_value = ['item2']
        self.assertEqual(main(user, cafe), ['item2'])

        # The user has not liked any item.
        mock_get_user_likes.return_value = []
        mock_meal_not_consumed.return_value = set()
        mock_most_liked_items.return_value = ['item1']
        self.assertEqual(main(user, cafe), ['item1'])
    
    # At least one item in the cafe and the user has liked some items.
    @patch('recommender_systems.utils.utilitaries.regroup_by_cluster')
    @patch('recommender_systems.systems.items_recommenders.content_based_filtering.favorite_cluster')
    @patch('recommender_systems.systems.items_recommenders.content_based_filtering.remove_cluster')
    def test_algorithm(self, mock_remove_cluster, mock_favorite_cluster, mock_regroup_by_cluster):
        user = {'user_id': 'user1', 'username': 'username1'}
        cafe = {
            'menu_items': [
                {
                    'slug': 'item1',
                    'likes': ['user1', 'user2', 'user3']
                }, 
                {
                    'slug': 'item2',
                    'likes': ['user5', 'user6', 'user7', 'user8', 'user9']
                },
                {
                    'slug': 'item3',
                    'likes': []
                },
                {
                    'slug': 'item4',
                    'likes': ['user4', 'user1']
                },
                {
                    'slug': 'item5',
                    'likes': ['user4', 'user1', 'user3']
                }
            ]
        }
        items_not_bought = set([
            'item2', 'item4'
        ])

        mock_regroup_by_cluster.return_value = {
            '0': ['item1', 'item4'],
            '1': ['item2', 'item5'],
            '2': ['item3']
        }
        mock_favorite_cluster.side_effect = [
            {
                '0': ['item1', 'item4']
            }, 
            {
                '1': ['item2', 'item5']
            },
            {
                '2': ['item3']
            }
        ]
        mock_remove_cluster.side_effect = [
            {
                '0': ['item1', 'item4']
            }, 
            {
                '1': ['item2', 'item5']
            },
            {
                '2': ['item3']
            }
        ]

        self.assertEqual(sorted(algorithm(user, cafe, items_not_bought), reverse=True ), ['item4', 'item2'])

if __name__ == '__main__':
    unittest.main()