### Algorithme 4.1 ###
import random
import numpy as np
from sklearn.metrics import jaccard_score
from sklearn.metrics.pairwise import cosine_similarity
import time 

# Collaborative filtering algorithm.
# Recommand foods based on the similarity between the users.
def main(users: list, user) -> list:
    recommendations = []
    similarity_threshold = 0.75
    n_users = len(users)
    if n_users == 0:
        return []
    elif n_users == 1:
        return user.likes
    elif n_users > 1:
        S = []
        for _ in range(n_users):
            rand_user = users[random.randint(0, n_users-1)]
            if rand_user.user_id not in S and rand_user.user_id != user.user_id:
                S.append(rand_user)
        user_list = [user.likes, user.purchase_history, user.visited_cafe]
        for u in S:
            other_user_list = [u.likes, u.purchase_history, u.visited_cafe]
            J = []
            for i in range(0, len(other_user_list)):
                resized_array = resize(user_list[i], other_user_list[i])
                j = jaccard_score(np.array(resized_array[0]), np.array(resized_array[1]), average="weighted")
                J.append(j)
            #print(similarity_threshold)
            score = sum(J)
            if score >= similarity_threshold:
                np_user_0, np_user_1 = np.array(user_list[0]), np.array(user_list[1])
                np_other_user_0, np_other_user_1 = np.array(other_user_list[0]), np.array(other_user_list[1])
                u_union = np.union1d(np_user_0, np_user_1)
                other_u_union = np.union1d(np_other_user_0, np_other_user_1)
                diff_1 = np.setdiff1d(u_union, other_u_union)
                diff_2 = np.setdiff1d(other_u_union, u_union)
                diff_1 = list(diff_1)
                diff_2 = list(diff_2)
                diff_1.extend(diff_2)
                recommendations.append(diff_1)

        if len(recommendations) > 0:
            set_recommendations = set(recommendations[0])
            if len(recommendations) == 1:
                return recommendations
            for elem in recommendations[1:]:
                set_recommendations.union(elem)
            list_rec = list(set_recommendations)
            return [item for item in list_rec if item != '0']
        else:
            return []
        
def resize(A: list, B: list):
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