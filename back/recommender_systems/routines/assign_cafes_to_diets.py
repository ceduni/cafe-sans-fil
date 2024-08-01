from typing import List, Dict
from app.models.cafe_model import Cafe
from recommender_systems.utils import db_utils as DButils
from recommender_systems.utils.api_calls import UserApi, AuthApi
from tqdm import tqdm

#TODO: Add tests
def find_cafes_selling_diet_products(diet: Dict[str, str | List[str]], cafe_list: List[Cafe]) -> Dict[str, str | List[str]]:
    result = set()
    for cafe in cafe_list:
        items = DButils.get_cafe_items(cafe['slug'])
        for item in items:
            forbidden_foods_lower = set( map( lambda x: x.lower(), diet['forbidden_foods']) )
            ingredents_lower = set( map( lambda x: x.lower(), item['ingredients']) )
            if len(forbidden_foods_lower & ingredents_lower) == 0:
                result.add(cafe['slug'])
                break

    return list(result)

# def main():
#     all_cafes = DButils.get_all_cafe()
#     all_users = DButils.get_all_users()
#     result = {}
#     for _, user in enumerate(tqdm(all_users, desc="Assigning cafes to user diets")):
#         result[user['username']] = user['username']
#         for i in range(len(diet_list)):
#             updated_diet = find_cafes_selling_diet_products(diet_list[i], all_cafes)
#             diet_list[i] = updated_diet
        
#         user['diet_profile']['diets'] = diet_list

#         UserApi.update_user(auth_token=AuthApi.auth_login(), username=user['username'], json_data=user)
