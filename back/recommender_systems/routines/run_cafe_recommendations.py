from recommender_systems.systems.cafe_recommenders import collaborative
from recommender_systems.systems.cafe_recommenders import content_based
from app.models.user_model import User
from app.models.cafe_model import Cafe
from recommender_systems.utils import db_utils as DButils
from typing import List, Dict
from recommender_systems.utils.api_calls import CafeRecommenderApi, AuthApi
from tqdm import tqdm

# Run cafe recommendations for all users.
def _run_cafe_recommendations() -> Dict[str, List[str]]:
    users: list[User] = DButils.get_all_users()
    all_cafe: list[Cafe] = DButils.get_all_cafe()
    recommendations: dict[str, list[str]] = {}
    try:
        for _, user in enumerate( tqdm(users, desc="Running cafe recommendations") ):
            recommendations[user['user_id']] = collaborative.main(users, user).extend( content_based.main(all_cafe, user) )
        return recommendations
    except ValueError as e:
        print(e)
        return {}

# Update cafe recommendations for all users.
def update_cafe_recommendations():
    auth_token = AuthApi.auth_login()
    recommendations: dict[str, list[str]] = _run_cafe_recommendations()
    if recommendations != {}:
        for _, user_id in enumerate( tqdm(recommendations.keys(), desc="Updating cafe recommendations") ):
            data = {
                "recommendations": recommendations[user_id]
            }
            CafeRecommenderApi.update_user_cafe_recommendations(auth_token=auth_token, user_id=user_id, json_data=data)