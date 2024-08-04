from recommender_systems.systems.cafe_recommenders import collaborative
from recommender_systems.systems.cafe_recommenders import content_based
from app.models.user_model import User
from app.models.cafe_model import Cafe
from recommender_systems.utils import db_utils as DButils
from typing import List, Dict
from recommender_systems.utils.api_calls import AuthApi, RecommendationsApi
from tqdm import tqdm

# Run cafe recommendations for all users.
def _run_cafe_recommendations() -> Dict[str, List[str]]:
    users: list[User] = DButils.get_all_users()
    all_cafe: list[Cafe] = DButils.get_all_cafe()
    recommendations: dict[str, list[str]] = {}
    try:
        for _, user in enumerate( tqdm(users, desc="Finding cafe recommendations") ):
            user_recommendations = []
            if user['first_name'] == "Tom":
                content_based_recs: list[str] = content_based.main(all_cafe=all_cafe, user=user)
                collab_based_recs: list[str] = collaborative.main(users=users, user=user)
                user_recommendations.extend(content_based_recs)
                user_recommendations.extend(collab_based_recs)
                recommendations[user['username']] = list( set(user_recommendations) )
        return recommendations
    except ValueError as e:
        print(e)
        return recommendations

# Update cafe recommendations for all users.
def update_cafe_recommendations():
    auth_token = AuthApi.auth_login()
    recommendations: dict[str, list[str]] = _run_cafe_recommendations()
    print(recommendations)
    if recommendations != {}:
        for _, username in enumerate( tqdm(recommendations.keys(), desc="Updating cafe recommendations") ):
            user = DButils.get_user(username)
            _, status = RecommendationsApi.get_user(user_id=user["user_id"])
            if status != 200:
                data = {
                    "user_id": user['user_id'],
                    "username": username,
                    "cafe_recommendations": recommendations[username],
                    "personnal_recommendations": []
                }
            else:
                data = {
                    "cafe_recommendations": recommendations[username],
                }
            #CafeRecommenderApi.update_user_cafe_recommendations(auth_token=auth_token, user_id=user.user_id, json_data=data)
            RecommendationsApi.update_user_cafe_recommendations(auth_token=auth_token, user_id=user['user_id'], json_data=data)