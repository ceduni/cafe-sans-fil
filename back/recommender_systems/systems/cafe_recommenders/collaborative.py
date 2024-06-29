from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
from app.models.cafe_model import Cafe, MenuItem
from app.models.user_model import User
from typing import List

async def main(users: List[User], user: User) -> List[str]:
    users.remove(user)
    similarities: list[float] = []
    user_visited_cafe: List[str] = await DButils.get_user_visited_cafe(user)
    user_list: list[list[str]] = [ await DButils.get_user_likes(user), await DButils.get_user_orders(user), user_visited_cafe ]
    for other_user in users:
        other_user_list: list[list[str]] = [ await DButils.get_user_likes(other_user), await DButils.get_user_orders(other_user), await DButils.get_user_visited_cafe(other_user) ]
        similarities.append(Utilitaries.users_similarity(user_list, other_user_list))
    
    n_best_users: int = round(0.75*len(similarities))
    sim_users_cafes: set[str] = set()
    for _ in range(n_best_users):
        max_sim: float = max(similarities)
        index: int = similarities.index(max_sim)
        found_user: User = users[index]
        visited_cafes: List[str] = await DButils.get_user_visited_cafe(found_user)
        sim_users_cafes.union( set(visited_cafes) )

    recommendations_set: set[str] = sim_users_cafes.difference(set(user_visited_cafe))

    return list(recommendations_set)