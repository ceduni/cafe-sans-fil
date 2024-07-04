import unittest
from unittest.mock import MagicMock
from typing import List

from app.models.user_model import User
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils

from recommender_systems.systems.items_recommenders.collaborative_filtering import *

'''
Note: The order of application of the @patch decorators (bottom to top) corresponds to the order
in which the mocked objects are passed as arguments to the test method, from left to right.
'''

#TODO
class TestCollaborativeFiltering(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()