from typing import List, Tuple, Dict

from app.models.cafe_model import Cafe, MenuItem
from recommender_systems.utils import db_utils as DButils
from app.models.user_model import User
import random
from tqdm import tqdm

# Tuple: (number of items liked, cafe_slug )
def score_cafe(list_cafe: List[Cafe], user: User) -> List[Tuple[int, str]]:
    scored_cafes: list[tuple[int, str]] = [] 
    for cafe in list_cafe:
        items: list[MenuItem] = DButils.get_cafe_items(cafe['slug'])
        count: int = 0
        for item in items:
            user_likes = DButils.get_user_likes_in_cafe(user['user_id'], items)
            if item['slug'] in user_likes:
                count += 1
        scored_cafes.append( (count, cafe['slug']) )
    return scored_cafes

def get_best_cafe(list_cafe: List[Cafe], user: User, n_cafes: int = 10) -> Dict[str, float]:
    sorted_cafes: list[tuple[int, str]] = sorted(score_cafe(list_cafe, user), reverse=True)
    result: dict[str, float] = {}
    if n_cafes > len(sorted_cafes):
        n_cafes = len(sorted_cafes)

    for t in sorted_cafes:
        result[t[1]] = t[0]

    #return [ sorted_cafes[i][1] for i in range(n_cafes) ]
    return result

# Always return one recommendation if the user did not like any item yet.
# Return cafe slugs.
def main(all_cafe: List[Cafe], user: User, n_recommendation: int = 10) -> Dict[str, float]:
    if user is None or isinstance(user, dict) == False:
        raise ValueError("User must be defined")
    user_likes = list( set(DButils.get_all_user_likes(user['username'])) )
    if len(user_likes) == 0:
        if all_cafe is None or len(all_cafe) == 0:
            return {}
        return all_cafe[random.randint(0, len(all_cafe)-1)]['slug'] # Return a random cafe
    else:
        if all_cafe is None or len(all_cafe) == 0:
            return {}
        return get_best_cafe(all_cafe, user, n_recommendation)
