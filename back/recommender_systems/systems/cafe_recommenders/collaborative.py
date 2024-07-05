from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
from app.models.user_model import User
from typing import List

def main(users: List[User], user: User) -> List[str]:

    if user is None:
        raise ValueError("User must be defined")

    if len(users) == 0:
        return DButils.get_user_visited_cafe(user)
    
    users.remove(user) if user in users else None
    similarities: list[float] = []
    user_visited_cafe: List[str] = DButils.get_user_visited_cafe(user)
    user_list: list[list[str]] = [ DButils.get_user_likes(user['id']), DButils.get_user_orders(user), user_visited_cafe ]
    for other_user in users:
        other_user_list: list[list[str]] = [ DButils.get_user_likes(other_user['id']), DButils.get_user_orders(other_user), DButils.get_user_visited_cafe(other_user) ]
        similarities.append(Utilitaries.users_similarity(user_list, other_user_list))
    
    n_best_users: int = round(0.75*len(similarities))
    sim_users_cafes: list[str] = []
    
    for _ in range(n_best_users):
        max_sim: float = max(similarities)
        index: int = similarities.index(max_sim)
        found_user: User = users[index]
        visited_cafes: list[str] = DButils.get_user_visited_cafe(found_user)
        sim_users_cafes.extend( visited_cafes )
        similarities[index] = -1

    set_sim_users_cafes: set[str] = set(sim_users_cafes)
    recommendations_set: set[str] = set_sim_users_cafes.difference(set(user_visited_cafe))

    return list(recommendations_set)