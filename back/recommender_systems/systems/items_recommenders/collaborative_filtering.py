### Algorithme 4.1 ###
from app.models.user_model import User
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
from typing import List

# Collaborative filtering algorithm.
# Recommand foods based on the similarity between the users.
def main(users: List[User], user: User, similarity_threshold: float= 0.5) -> List[str]:
    recommendations: list[list[str]] = []
    n_users: int = len(users)

    if user == None:
        raise ValueError('User should not be None')
    
    if n_users >= 1:
        if n_users > 1 and users[0]['user_id'] != user['user_id']:
            users_copy = users[:]
            users_copy.remove(user) if user in users_copy else None
            other_users = users_copy

            items_in_orders: list[str] = Utilitaries.list_items( DButils.get_user_orders(user) )
            user_likes: List[str] = DButils.get_all_user_likes(user['username'])
            user_visited_cafe: List[str] = DButils.get_user_visited_cafe(user)
            user_list: list[set[str]] = [ set(user_likes), set(items_in_orders), set(user_visited_cafe) ]

            for u in other_users:
                other_items_in_orders: list[str] = Utilitaries.list_items( DButils.get_user_orders(u))
                other_user_list: list[set[str]] = [
                    set( DButils.get_all_user_likes(u['username']) ), 
                    set(other_items_in_orders), 
                    set( DButils.get_user_visited_cafe(u) )
                ]
                score: float = Utilitaries.users_similarity(user_list, other_user_list)
                if score >= similarity_threshold:
                    u_union: set = user_list[0].union(user_list[1])
                    other_u_union: set = other_user_list[0].union(other_user_list[1])
                    diff: set = other_u_union.difference(u_union)
                    recommendations.append(list(diff))

            if len(recommendations) > 0:
                set_recommendations: set = set(recommendations[0]) # Remove redundant items.
                if len(recommendations) == 1:
                    return list(set_recommendations)
                for elem in recommendations[1:]:
                    set_recommendations = set_recommendations.union(set(elem))
                return [item for item in set_recommendations if item != '0']
            else:
                return []
        else:
            return DButils.get_all_user_likes(user['username'])
    else:
        return DButils.get_all_user_likes(user['username'])