from utils import utilitaries as Utilitaries
from app.models.user_model import User
from app.models.cafe_model import Cafe, MenuItem
from typing import List

def tes_reshape():
    A: list[str] = ['This', 'Is']
    B: list[str] = ['A', 'Test']
    C: list[str] = ['For', 'This', 'Code']

    assert Utilitaries.reshape(A,B) == (A, B)
    assert Utilitaries.reshape(B,C) == (['A', 'Test', '0'], C)
    assert Utilitaries.reshape(C,A) == (C, ['This', 'Is', '0'])

def test_items_slugs(items: List[MenuItem]):
    slugs: list[str] = []
    for item in items:
        slugs.append(item.slug)

    assert Utilitaries.items_slugs([items[0]])[0] == slugs[0] # Check for one item
    assert Utilitaries.items_slugs(items) == slugs # Check for many items

def test_list_items(orders_ids: List[str], action: str):
    pass

def test_meal_not_consumed(cafe: Cafe, user: User):
    pass