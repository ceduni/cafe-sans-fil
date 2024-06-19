### Algorithme 4.1 ###
from app.models.user_model import User
import utilitaries as Utilitaries

import random
import numpy as np
from sklearn.metrics import jaccard_score
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Any, Tuple

def reshape(A: List[Any], B: List[Any]) -> Tuple[List[Any]]:
    if len(A) == len(B):
        return (A, B)
    elif len(A) < len(B):
        for _ in range(len(B) - len(A)):
            A.append('0')
        return (A, B)
    else:
        for _ in range(len(A) - len(B)):
            B.append('0')
        return (A, B)       

# Collaborative filtering algorithm.
# Recommand foods based on the similarity between the users.
async def main(users: List[User], user: User) -> List[str]:
    recommendations: list[list[str]] = []
    similarity_threshold: float = 0.75
    n_users: int = len(users)
    if n_users == 0:
        return []
    elif n_users == 1:
        return user.likes
    elif n_users > 1:
        S: list[User] = []
        for _ in range(n_users):
            rand_user: User = users[random.randint(0, n_users-1)]
            if str(rand_user.id) not in S and str(rand_user.id) != str(user.id):
                S.append(rand_user)

        items_in_orders: list[str] = await Utilitaries.list_items_bought(user.order_history, "ids")
        user_list: list[list[str]] = [user.likes, items_in_orders, user.visited_cafe]
        for u in S:
            other_items_in_orders: list[str] = await Utilitaries.list_items_bought(u.order_history, "ids")
            other_user_list: list[list[str]] = [u.likes, other_items_in_orders, u.visited_cafe]
            J: list[float] = []
            for i in range(0, len(other_user_list)):
                resized_array: tuple[list[str]] = reshape(user_list[i], other_user_list[i])
                j: float = jaccard_score(np.array(resized_array[0]), np.array(resized_array[1]), average="weighted")
                J.append(j)
            score: float = sum(J)
            if score >= similarity_threshold:
                np_user_0: np.array[str] = np.array(user_list[0])
                np_user_1: np.array[str] = np.array(user_list[1])
                np_other_user_0: np.array[str] = np.array(other_user_list[0])
                np_other_user_1: np.array[str] = np.array(other_user_list[1])
                u_union: np.array[str] = np.union1d(np_user_0, np_user_1)
                other_u_union: np.array[str] = np.union1d(np_other_user_0, np_other_user_1)
                diff_1: np.array[str] = np.setdiff1d(u_union, other_u_union)
                diff_2: np.array[str] = np.setdiff1d(other_u_union, u_union)
                diff_1: np.array[str] = list(diff_1)
                diff_2: np.array[str] = list(diff_2)
                diff_1.extend(diff_2)
                recommendations.append(diff_1)

        if len(recommendations) > 0:
            set_recommendations: set[str] = set(recommendations[0]) # Remove redondant items.
            if len(recommendations) == 1:
                return list(set_recommendations)
            for elem in recommendations[1:]:
                set_recommendations.union(set(elem))
            list_rec: list[str] = list(set_recommendations)
            return [item for item in list_rec if item != '0']
        else:
            return []