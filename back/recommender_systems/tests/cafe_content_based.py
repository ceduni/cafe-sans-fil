from recommender_systems.systems.cafe_recommenders.content_based import *
import unittest
from unittest.mock import patch, MagicMock, Mock

class TestMain(unittest.TestCase):

    @patch('recommender_systems.utils.db_utils.get_cafe_items')
    @patch('recommender_systems.utils.db_utils.get_user_likes')
    def test_score_cafe(self, mock_get_user_likes, mock_get_cafe_items):
        # Test with 0 cafes
        mock_get_cafe_items.return_value = []
        mock_get_user_likes.return_value = []
        result = score_cafe([], {'id': 'user_test'})
        self.assertEqual(result, [])

        # No items liked by the user
        mock_get_cafe_items.return_value = [{'slug': 'item1'}, {'slug': 'item2'}]
        mock_get_user_likes.return_value = []
        result = score_cafe([{'slug': 'cafe1'}], {'id': 'user_test'})
        self.assertEqual(result, [(0, 'cafe1')])

        # Test with cafes and some liked items
        mock_get_cafe_items.side_effect = [
            [{'slug': 'item3'}, {'slug': 'item2'}],
            [{'slug': 'item1'}, {'slug': 'item4'}]
        ]
        mock_get_user_likes.return_value = ['item1']
        result = score_cafe([{'slug': 'cafe1'}, {'slug': 'cafe2'}], {'id': 'user_test'})
        self.assertEqual(result, [(0, 'cafe1'), (1, 'cafe2')])

        # Test with no likes for some cafes
        mock_get_cafe_items.side_effect = [
            [{'slug': 'item1'}, {'slug': 'item2'}],
            [{'slug': 'item2'}, {'slug': 'item4'}]
        ]
        mock_get_user_likes.return_value = ['item1', 'item3']
        result = score_cafe([{'slug': 'cafe1'}, {'slug': 'cafe2'}], {'id': 'user_test'})
        self.assertEqual(result, [(1, 'cafe1'), (0, 'cafe2')])
        
    @patch('recommender_systems.systems.cafe_recommenders.content_based.score_cafe')
    def test_get_best_cafe(self, mock_score_cafe):
        # Test 1: Normal.
        mock_score_cafe.return_value = [(0, 'cafe1'), (1, 'cafe2')]
        result = get_best_cafe([{'slug': 'cafe1'}, {'slug': 'cafe2'}], {'id': 'user_test'})
        self.assertEqual(result, ['cafe2'])

        # Test 2: Two cafes with the same score.
        mock_score_cafe.return_value = [(1, 'cafe1'), (1, 'cafe2')]
        result = get_best_cafe([{'slug': 'cafe1'}, {'slug': 'cafe2'}], {'id': 'user_test'})
        self.assertEqual(result, ['cafe2'])

        # Test 3: 5 cafes.
        mock_score_cafe.return_value = [(57, 'cafe1'), (32, 'cafe2'), (66, 'cafe3'), (12, 'cafe4'), (1, 'cafe5')]
        result = get_best_cafe([{'slug': 'cafe1'}, {'slug': 'cafe2'}, {'slug': 'cafe3'}, {'slug': 'cafe4'}, {'slug': 'cafe5'}], {'id': 'user_test'}, 3)
        self.assertEqual(sorted(result, reverse=False), ['cafe1', 'cafe2', 'cafe3'])

        # Test 4: No cafes scored.
        mock_score_cafe.return_value = []
        result = get_best_cafe([{'slug': 'cafe1'}, {'slug': 'cafe2'}], {'id': 'user_test'}, 5)
        self.assertEqual(result, [])

        # Test 5: No cafes
        mock_score_cafe.return_value = []
        result = get_best_cafe([], {'id': 'user_test'}, 5)
        self.assertEqual(result, [])

    @patch('recommender_systems.systems.cafe_recommenders.content_based.get_best_cafe')
    @patch('recommender_systems.utils.db_utils.get_user_likes')
    def test_main(self, mock_get_user_likes, mock_get_best_cafe):
        # Test 1: No cafes and no liked items
        mock_get_user_likes.return_value = []
        mock_get_best_cafe.return_value = []
        result = main([], {'id': 'user_test'})
        self.assertEqual(result, [])

        # Test 2: Some cafes and no liked items
        mock_get_user_likes.return_value = []
        mock_get_best_cafe.return_value = []
        result = main([{'slug': 'cafe1'}, {'slug': 'cafe2'}], {'id': 'user_test'})
        self.assertNotEqual(result, [])

        # Test 3: Some liked items but no cafes
        mock_get_user_likes.return_value = ['item1']
        mock_get_best_cafe.return_value = []
        result = main([], {'id': 'user_test'})
        self.assertEqual(result, [])

        # Test 4: Some liked items and some cafes
        mock_get_user_likes.return_value = ['item1']
        mock_get_best_cafe.return_value = ['cafe1']
        result = main([{'slug': 'cafe1'}, {'slug': 'cafe2'}], {'id': 'user_test'})
        self.assertEqual(result, ['cafe1'])

if __name__ == '__main__':
    unittest.main()