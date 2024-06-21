from systems import collaborative_filtering as CB
from app.models.user_model import User
from typing import List

# Test cases for 0 and 1 user.
def test_main_1(user: User):
    assert CB.main([], user) == user.likes
    assert CB.main([user], user) == user.likes

# Test cases for more than 1 user.
def test_main_2(users: List[User], user: User):
    pass
