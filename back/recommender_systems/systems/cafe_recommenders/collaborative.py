from recommender_systems.utils import utilitaries as Utilitaries
from app.models.cafe_model import Cafe, MenuItem
from app.models.user_model import User
from typing import List

def main(users: List[User], user: User) -> List[str]:
    users.remove(user)
    similarities: list[float] = []
    for other_user in users:
        similarities.append(Utilitaries.users_similarity(user, other_user))
    

    n_best_users: int = round(0.75*len(similarities))
    sim_users_cafes: set[str] = set()
    for _ in range(n_best_users):
        max_sim: float = max(similarities)
        index: int = similarities.index(max_sim)
        sim_users_cafes.append(users[index].visited_cafe)

    user_cafe_set: set[str] = set(user.visited_cafe)

    recommendations_set: set[str] = sim_users_cafes.difference(user_cafe_set)

    return list(recommendations_set)