from recommender_systems.utils.utilitaries import *
import unittest
from unittest.mock import patch

'''
Note: The order of application of the @patch decorators (bottom to top) corresponds to the order
in which the mocked objects are passed as arguments to the test method, from left to right.
'''

class TestUtilitaries(unittest.TestCase):

    def test_jaccard_similarity(self):
        A = set(['A', 'B', 'C'])
        B = set(['B', 'C', 'D'])
        C = set(['C', 'D', 'E'])

        self.assertEqual(jaccard_similarity(A, B), 0.5)
        self.assertEqual(jaccard_similarity(A, C), 0.2)
        self.assertEqual(jaccard_similarity(A, A), 1)
        self.assertEqual(jaccard_similarity(B, C), 0.5)

    def test_users_similarity(self):
        u_list = [['A', 'B', 'C'], ['B', 'C', 'D'], ['C', 'D', 'E']]
        v_list = [['A', 'B', 'C'], ['B', 'C', 'D'], ['C', 'D', 'E']]

        u_list_2 = [['A', 'B', 'C'], ['B', 'C', 'D'], ['C', 'D', 'E']]
        v_list_2 = [['E', 'D', 'G'], ['G', 'H', 'I'], ['A', 'B', 'H']]

        u_list_3 = [['A', 'B', 'C'], ['B', 'C', 'D'], ['C', 'D', 'E']]
        v_list_3 = [['D', 'B', 'E'], ['A', 'C', 'E'], ['C', 'F', 'G']]

        self.assertEqual(round(users_similarity(u_list, v_list), 1), 3)
        self.assertEqual(round(users_similarity(u_list_2, v_list_2), 1), 0)
        self.assertEqual(round(users_similarity(u_list_3, v_list_3), 1), 0.6)

    def test_sort_items_by_occurences(self):
        map = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

        self.assertEqual(sort_items_by_occurences(map), ['d', 'c', 'b', 'a'])

    def test_most_bought_items(self):
        orders = [
            {'items': [{'item_slug': 'a'}, {'item_slug': 'b'}, {'item_slug': 'c'}]},
            {'items': [{'item_slug': 'b'}, {'item_slug': 'c'}, {'item_slug': 'd'}]},
            {'items': [{'item_slug': 'c'}, {'item_slug': 'd'}, {'item_slug': 'e'}]},
        ]

        self.assertEqual(most_bought_items(orders), ['c', 'd', 'b', 'e', 'a'])

    def test_most_liked_items(self):
        items = [
            {'slug': 'a', 'likes': ['1', '2', '3', '4', '5', '6']},
            {'slug': 'b', 'likes': ['1', '2', '3', '4', '5', '6', '7']},
            {'slug': 'c', 'likes': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']},
            {'slug': 'd', 'likes': ['1', '2', '3', '4', '5', '6', '7', '8', '9']},
        ]

        self.assertEqual(most_liked_items(items), ['c', 'd', 'b', 'a'])
        self.assertEqual(most_liked_items(items, 2), ['c', 'd'])

    @patch('recommender_systems.utils.api_calls.OrderApi.get_order')
    def test_list_items(self, mock_get_order):
        # Test 1: Normal case
        orders_id = ["order1", "order2"]
        mock_get_order.side_effect = [
            ({
                'items': [
                    {'slug': 'item1'}, 
                    {'slug': 'item2'}, 
                    {'slug': 'item3'},
                ]
            }, 200),
            ({
                'items': [
                    {'slug': 'item4'}, 
                    {'slug': 'item5'}, 
                    {'slug': 'item6'},
                ]
            }, 200)
        ]

        self.assertEqual(list_items(orders_id), ['item1', 'item2', 'item3', 'item4', 'item5', 'item6'])

        # Test 2: Empty list
        mock_get_order.return_value = {'items': []}
        self.assertEqual(list_items([]), [])
        
    def test_regroup_by_cluster(self):
        items = [
            {'slug': 'a', 'cluster': '0'},
            {'slug': 'b', 'cluster': '1'},
            {'slug': 'c', 'cluster': '0'},
            {'slug': 'd', 'cluster': '3'},
            {'slug': 'h', 'cluster': '1'},
            {'slug': 'g', 'cluster': '2'},
            {'slug': 'f', 'cluster': '3'},
            {'slug': 'z', 'cluster': '4'},
        ]

        self.assertEqual(regroup_by_cluster(items), {'0': ['a', 'c'], '1': ['b', 'h'], '2': ['g'], '3': ['d', 'f'], '4': ['z']})

    @patch('recommender_systems.utils.api_calls.CafeApi.get_item')
    def test_filter_items_by_cafe(self, mock_get_item):
        # Test 1: Return unique items
        mock_get_item.side_effect = [
            {'slug': 'item1'},
            {'slug': 'item2'},
            {'slug': 'item3'},
            {'slug': 'item4'},
            {'slug': 'item5'}
        ]
        slugs = ['item1', 'item2', 'item3', 'item4', 'item5']
        cafe_slug = 'cafe1'
        expected_result = ['item1', 'item2', 'item3', 'item4', 'item5']
        result = filter_items_by_cafe(slugs, cafe_slug)
        self.assertEqual(result, expected_result)

        # Test 2: Filter items
        mock_get_item.side_effect = [
            {'slug': 'item1'},
            None,
            {'slug': 'item3'},
            {'slug': 'item4'},
            {'slug': 'item5'}
        ]
        slugs = ['item1', 'item2', 'item3', 'item4', 'item5']
        cafe_slug = 'cafe1'
        expected_result = ['item1', 'item3', 'item4', 'item5']
        result = filter_items_by_cafe(slugs, cafe_slug)
        self.assertEqual(result, expected_result)

        # Test 3: Return empty list if no items
        mock_get_item.side_effect = [None, None, None, None, None]
        slugs = ['item1', 'item2', 'item3', 'item4', 'item5']
        cafe_slug = 'cafe1'
        expected_result = []
        result = filter_items_by_cafe(slugs, cafe_slug)
        self.assertEqual(result, expected_result)

    def test_find_indexes(self):
        items = ['a', 'b', 'a', 'c', 'd', 'd', 'e', 'd']

        self.assertEqual(find_indexes(items, 'a'), [0, 2])
        self.assertEqual(find_indexes(items, 'b'), [1])
        self.assertEqual(find_indexes(items, 'c'), [3])
        self.assertEqual(find_indexes(items, 'd'), [4, 5, 7])
        self.assertEqual(find_indexes(items, 'e'), [6])

    def test_health_score(self):
        item = {
            'nutritional_informations': {
                'calories': 10,
                'protein': 100,
                'carbohydrates': 2,
                'lipid': 3,
                'saturated_fat': 4,
                'sodium': 5,
                'sugar': 0,
                'fiber': 700,
                'percentage_fruit_vegetables_nuts': 800,
                'vitamins': 900
            }
        }

        self.assertEqual(health_score(item), -6)

    def test_reshape(self):
        A = [1, 2, 3, 4, 5, 6]
        B = [7, 5, 9]
        
        self.assertEqual(reshape(A, B), (A, [7, 5, 9, '0', '0', '0']))

class TestFindCafe(unittest.TestCase):
    def setUp(self):
        # Set up test data for test_find_cafe
        self.cafe1 = {'slug': 'cafe1'}
        self.cafe2 = {'slug': 'cafe2'}
        self.item1 = {'slug':'item1'}
        self.item2 = {'slug': 'item2'}
        self.cafe_list = [self.cafe1, self.cafe2]

    @patch('recommender_systems.utils.utilitaries.items_slugs')
    @patch('recommender_systems.utils.db_utils.get_cafe_items')
    def test_1(self, mock_get_cafe_items, mock_items_slugs):
        # Test when the item is in the cafe
        mock_get_cafe_items.side_effect = [[self.item1], [self.item2]]
        mock_items_slugs.side_effect = [['item1'], ['item2']]
        result = find_cafe_by_item(self.cafe_list, self.item1)
        self.assertEqual(result, [self.cafe1])

    @patch('recommender_systems.utils.utilitaries.items_slugs')
    @patch('recommender_systems.utils.db_utils.get_cafe_items')
    def test_2(self, mock_get_cafe_items, mock_items_slugs):
        # Test when the item is not in the cafe
        mock_get_cafe_items.return_value = [self.item2]
        mock_items_slugs.return_value = ['item2']
        result = find_cafe_by_item(self.cafe_list, self.item1)
        self.assertEqual(result, [])

    def test_3(self):
        # Test when the cafe list is empty
        result = find_cafe_by_item([], self.item1)
        self.assertEqual(result, [])

    def test_4(self):
        # Test when the item is None
        result = find_cafe_by_item(self.cafe_list, None)
        self.assertEqual(result, [])

    def test_5(self):
        # Test when the cafe list is None
        result = find_cafe_by_item(None, self.item1)
        self.assertEqual(result, [])

class TestMealNotConsumed(unittest.TestCase):

    def test_1(self):
        self.assertEqual(meal_not_consumed(None, None), [])
        self.assertEqual(meal_not_consumed(None, {'id': 'user1'}), [])
        self.assertEqual(meal_not_consumed({'slug': 'cafe1'}, None), [])

    @patch('recommender_systems.utils.db_utils.get_cafe_items')
    @patch('recommender_systems.utils.utilitaries.items_slugs')
    @patch('recommender_systems.utils.db_utils.get_user_orders')
    @patch('recommender_systems.utils.db_utils.get_order')
    @patch('recommender_systems.utils.db_utils.get_order_items')
    def test_2(self, mock_get_order_items, mock_get_order, mock_get_user_orders, mock_items_slugs, mock_get_cafe_items):
        mock_get_cafe_items.return_value = [{'slug': 'item1'}, {'slug': 'item2'}]
        mock_items_slugs.return_value = ['item1', 'item2', 'item3', 'item4', 'item5']
        mock_get_user_orders.return_value = ['order1', 'order2']
        mock_get_order.side_effect = [
            {'cafe_slug': 'cafe1'},
            {'cafe_slug': 'cafe2'},
        ]
        mock_get_order_items.side_effect = [
            ['item1', 'item2'],
            ['item3', 'item4', 'item6', 'item7', 'item8'],
        ]
        result = meal_not_consumed({'slug': 'cafe1'}, {'id': 'user1'})
        self.assertIn('item3', result)
        self.assertIn('item4', result)
        self.assertIn('item5', result)


if __name__ == "__main__":
    unittest.main()