from recommender_systems.utils import utilitaries as Utilitaries
import unittest

'''
Note: The order of application of the @patch decorators (bottom to top) corresponds to the order
in which the mocked objects are passed as arguments to the test method, from left to right.
'''

class TestUtilitaries(unittest.TestCase):

    def test_jaccard_similarity(self):
        A = set(['A', 'B', 'C'])
        B = set(['B', 'C', 'D'])
        C = set(['C', 'D', 'E'])

        self.assertEqual(Utilitaries.jaccard_similarity(A, B), 0.5)
        self.assertEqual(Utilitaries.jaccard_similarity(A, C), 0.2)
        self.assertEqual(Utilitaries.jaccard_similarity(A, A), 1)
        self.assertEqual(Utilitaries.jaccard_similarity(B, C), 0.5)

    def test_users_similarity(self):
        u_list = [['A', 'B', 'C'], ['B', 'C', 'D'], ['C', 'D', 'E']]
        v_list = [['A', 'B', 'C'], ['B', 'C', 'D'], ['C', 'D', 'E']]

        u_list_2 = [['A', 'B', 'C'], ['B', 'C', 'D'], ['C', 'D', 'E']]
        v_list_2 = [['E', 'D', 'G'], ['G', 'H', 'I'], ['A', 'B', 'H']]

        u_list_3 = [['A', 'B', 'C'], ['B', 'C', 'D'], ['C', 'D', 'E']]
        v_list_3 = [['D', 'B', 'E'], ['A', 'C', 'E'], ['C', 'F', 'G']]

        self.assertEqual(round(Utilitaries.users_similarity(u_list, v_list), 1), 3)
        self.assertEqual(round(Utilitaries.users_similarity(u_list_2, v_list_2), 1), 0)
        self.assertEqual(round(Utilitaries.users_similarity(u_list_3, v_list_3), 1), 0.6)

    def test_sort_items_by_occurences(self):
        map = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

        self.assertEqual(Utilitaries._sort_items_by_occurences(map), ['d', 'c', 'b', 'a'])

    def test_most_bought_items(self):
        orders = [
            {'items': [{'item_slug': 'a'}, {'item_slug': 'b'}, {'item_slug': 'c'}]},
            {'items': [{'item_slug': 'b'}, {'item_slug': 'c'}, {'item_slug': 'd'}]},
            {'items': [{'item_slug': 'c'}, {'item_slug': 'd'}, {'item_slug': 'e'}]},
        ]

        self.assertEqual(Utilitaries.most_bought_items(orders), ['c', 'd', 'b', 'e', 'a'])

    def test_most_liked_items(self):
        items = [
            {'slug': 'a', 'likes': ['1', '2', '3', '4', '5', '6']},
            {'slug': 'b', 'likes': ['1', '2', '3', '4', '5', '6', '7']},
            {'slug': 'c', 'likes': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']},
            {'slug': 'd', 'likes': ['1', '2', '3', '4', '5', '6', '7', '8', '9']},
        ]

        self.assertEqual(Utilitaries.most_liked_items(items), ['c', 'd', 'b', 'a'])
        self.assertEqual(Utilitaries.most_liked_items(items, 2), ['c', 'd'])

    #TODO
    def test_list_items(self):
        orders_id = [
            "9d22e803-d98a-4071-ae48-49c35a13dd53", # acqui-de-droit, order: 1
            "454dc4c9-8641-49c3-8c7a-d85323920900", # tore-et-fraction, order: 2
        ]

        #self.assertEqual(Utilitaries.list_items(orders_id), ["espresso", "jus-v8", "espresso-double", "latte-ou-cappucino", "gomme"])

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

        self.assertEqual(Utilitaries.regroup_by_cluster(items), {'0': ['a', 'c'], '1': ['b', 'h'], '2': ['g'], '3': ['d', 'f'], '4': ['z']})

    #TODO
    def test_filter_items_by_cafe(self):
        items = [
            "le-mozza",
            "le-marbre",
            "espresso",
            "espresso-double",
        ]

        cafe_slug_1 = "acquis-de-droit"
        cafe_slug_2 = "cafcom"

        # self.assertEqual(Utilitaries.filter_items_by_cafe(items, cafe_slug_1), ["le-mozza", "le-marbre", "espresso", "espresso-double"])
        # self.assertEqual(Utilitaries.filter_items_by_cafe(items, cafe_slug_2), ["le-mozza", "le-marbre", "espresso", "espresso-double"])

    #TODO
    def test_meal_not_consumed(self):
        pass

    #TODO
    def test_find_cafe_by_item(self):
        pass

    def test_find_indexes(self):
        items = ['a', 'b', 'a', 'c', 'd', 'd', 'e', 'd']

        self.assertEqual(Utilitaries.find_indexes(items, 'a'), [0, 2])
        self.assertEqual(Utilitaries.find_indexes(items, 'b'), [1])
        self.assertEqual(Utilitaries.find_indexes(items, 'c'), [3])
        self.assertEqual(Utilitaries.find_indexes(items, 'd'), [4, 5, 7])
        self.assertEqual(Utilitaries.find_indexes(items, 'e'), [6])

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

        self.assertEqual(Utilitaries.health_score(item), -6)

    def test_reshape(self):
        A = [1, 2, 3, 4, 5, 6]
        B = [7, 5, 9]
        
        self.assertEqual(Utilitaries.reshape(A, B), (A, [7, 5, 9, '0', '0', '0']))

if __name__ == "__main__":
    unittest.main()