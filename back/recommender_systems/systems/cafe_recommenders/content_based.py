from typing import List, Tuple

from app.models.cafe_model import Cafe, MenuItem
from recommender_systems.utils import db_utils as DButils
from app.models.user_model import User
import random

# Tuple: (number of items liked, cafe_slug )
def score_cafe(list_cafe: List[Cafe], user: User) -> List[Tuple[int, str]]:
    scored_cafes: list[tuple[int, str]] = [] 
    for cafe in list_cafe:
        items: list[MenuItem] = DButils.get_cafe_items(cafe['slug'])
        count: int = 0
        for item in items:
            if item['slug'] in DButils.get_user_likes(user['id']):
                count += 1
        scored_cafes.append( (count, cafe['slug']) )
    return scored_cafes

def get_best_cafe(list_cafe: List[Cafe], user: User, n_cafes: int = 1) -> List[str]:
    scored_cafes: list[tuple[int, str]] = score_cafe(list_cafe, user)
    sorted_cafes: list[tuple[int, str]] = sorted(scored_cafes, reverse=True)
    if n_cafes > len(sorted_cafes):
        n_cafes = len(sorted_cafes)
    return [ sorted_cafes[i][1] for i in range(n_cafes) ]

# Always return one recommendation if the user did not like any item yet.
# Return cafe slugs.
def main(all_cafe: List[Cafe], user: User, n_recommendation: int = 1) -> List[str]:
    if len(DButils.get_user_likes(user['id'])) == 0:
        if len(all_cafe) == 0:
            return []
        return all_cafe[random.randint(0, len(all_cafe)-1)] # Return a random cafe
    else:
        return get_best_cafe(all_cafe, user, n_recommendation)

