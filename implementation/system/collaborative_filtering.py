### Algorithme 4.1 ###
import random
import numpy as np
from sklearn.metrics import jaccard_score
from sklearn.metrics.pairwise import cosine_similarity
import time

### À supprimer ###
class Food:
    id = ""
    def __init__(self, id: str) -> None:
        self.id = id

class Cafe:
    id = ""
    def __init__(self, id: str) -> None:
        self.id = id
    
class User:
    user_id = ""
    consummed_foods = []
    visited_cafe = []
    likes = []

    def __init__(self, user_id: str, consummed_food: list[Food], visited_cafe: list[Cafe], likes: list[Food]) -> None:
        self.user_id = user_id
        self.consummed_foods = consummed_food
        self.visited_cafe = visited_cafe
        self.likes = likes

    def get_formatted_user(self):
        res = {
            "id": self.user_id,
            "consummed_foods": self.consummed_foods,
            "visited_cafe": self.visited_cafe,
            "likes": self.likes
        }
        return res

def generate_foods(k: int) -> list[Food]:
    foods = []
    for i in range(k):
        #id = uuid.uuid1()
        #foods.append(Food(str(id.int)))
        foods.append(Food(f'food_{i}'))
    return foods

def generate_cafes(k: int) -> list[Food]:
    cafes = []
    for i in range(k):
        #id = uuid.uuid1()
        #cafes.append(Cafe(str(id.int)))
        cafes.append(Cafe(f'cafe_{i}'))
    return cafes

def generate_users(foods: list[Food], cafes: list[Cafe], k: int) -> list[User]:
    users = []
    for i in range(k):
        n_cafes = random.randint(1, len(cafes) + 1)
        list_cafes = set()
        for _ in range(n_cafes):
            i_cafes = random.randint(0, len(cafes)-1)
            list_cafes.add(cafes[i_cafes])

        n_foods = random.randint(1, len(foods) + 1)
        set_food = set()
        for _ in range(n_foods):
            i_food = random.randint(0, len(foods)-1)
            set_food.add(foods[i_food])

        likes = []
        list_food = list(set_food)
        for i in range(len(list_food)//2):
            likes.append(list_food[i])

        users.append(User(f'{i}', list_food, list(list_cafes), likes))

    return users
### À SUpprimer ###

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
    
# Collaborative filtering algorithm.
# Recommand foods based on the similarity between the users.
def main(users: list[User], user: User) -> list[Food]:
    recommendations = []
    similarity_threshold = 0.75
    n_users = len(users)
    if n_users == 0:
        return []
    elif n_users == 1:
        return user.likes
    elif n_users > 1:
        #n = math.ceil(0.9*n_users)
        S = []
        for _ in range(n_users):
            rand_user = users[random.randint(0, n_users-1)]
            if rand_user.user_id not in S and rand_user.user_id != user.user_id:
                S.append(rand_user)
        user_list = [user.likes, user.consummed_foods, user.visited_cafe]
        for u in S:
            other_user_list = [u.likes, u.consummed_foods, u.visited_cafe]
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

### À supprimer ###
def generate_data():
    foods = generate_foods(20000)
    foods_db = []
    for food in foods:
        foods_db.append(food.id)

    cafes = generate_cafes(1000)
    cafes_db = []
    for cafe in cafes:
        cafes_db.append(cafe.id)

    users = generate_users(foods_db, cafes_db, 10000)
    return users

def test_algorithm():
    users = generate_data()
    if len(users) >= 1:
        user = users[0]
        #print(user.consummed_foods)
        #for u in users:
        #    print(u.get_formatted_user())
        start = time.time()
        res = main(users, user)
        end = time.time()
        print(res)
        print(f'Number of recommandations : {len(res)}')
        print(f'Time: {round(end - start, 2)}s')
    else:
        print("No user")

test_algorithm()
### À Supprimer ###