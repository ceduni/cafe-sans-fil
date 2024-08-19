from app.models.user_model import User
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
from typing import List, Tuple, Dict

# Collaborative filtering algorithm.
# Recommend foods based on the similarity between the users.
def main(users: List[User], user: User, similarity_threshold: float = 0.5) -> Dict[str, float]:
    recommendations: List[Tuple[str, float]] = []
    n_users: int = len(users)

    if user is None:
        raise ValueError('User should not be None')
    
    if n_users >= 1:
        if n_users > 1 and users[0]['user_id'] != user['user_id']:
            users_copy = users[:]
            users_copy.remove(user) if user in users_copy else None
            other_users = users_copy

            items_in_orders: List[str] = Utilitaries.list_items(DButils.get_user_orders(user))
            user_likes: List[str] = DButils.get_all_user_likes(user['username'])
            user_visited_cafe: List[str] = DButils.get_user_visited_cafe(user)
            user_list: List[set[str]] = [set(user_likes), set(items_in_orders), set(user_visited_cafe)]

            for u in other_users:
                other_items_in_orders: List[str] = Utilitaries.list_items(DButils.get_user_orders(u))
                other_user_list: List[set[str]] = [
                    set(DButils.get_all_user_likes(u['username'])), 
                    set(other_items_in_orders), 
                    set(DButils.get_user_visited_cafe(u))
                ]
                score: float = Utilitaries.users_similarity(user_list, other_user_list)
                if score >= similarity_threshold:
                    u_union: set = user_list[0].union(user_list[1])
                    other_u_union: set = other_user_list[0].union(other_user_list[1])
                    diff: set = other_u_union.difference(u_union)
                    recommendations.extend([(item, score) for item in diff])

            if recommendations:
                unique_recommendations = {}
                for item, score in recommendations:
                    if item in unique_recommendations:
                        unique_recommendations[item] = max(unique_recommendations[item], score)
                    else:
                        unique_recommendations[item] = score

                return unique_recommendations
            else:
                return {}
        else:
            likes = DButils.get_all_user_likes(user['username'])
            result = {}
            for item in likes:
                result[item] = 1.0
            return result
    else:
        likes = DButils.get_all_user_likes(user['username'])
        result = {}
        for item in likes:
            result[item] = 1.0
        return result
