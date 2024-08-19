from recommender_systems.systems.cafe_recommenders import collaborative
from recommender_systems.systems.cafe_recommenders import content_based
from app.models.user_model import User
from app.models.cafe_model import Cafe
from recommender_systems.utils import db_utils as DButils
from typing import List, Dict
from recommender_systems.utils.api_calls import AuthApi, RecommendationsApi
from tqdm import tqdm

#TODO: Add tests
def assign_final_scores(content_based_recs: Dict[str, float], collaborative_recs: Dict[str, float]) -> Dict[str, float]:
    result: dict[str, float] = {}
    for cafe, score in collaborative_recs.items():
        if cafe in content_based_recs:
            result[cafe] = 0.4 * content_based_recs[cafe] + 0.6 * score
        else:
            result[cafe] = score
    return result

#TODO: Add tests
def sort_cafe_recommendations(recommendations: Dict[str, float], n_recommendations: int = 5) -> List[str]:
    revesed_recommendations: dict[float, str] = {v: k for k, v in recommendations.items()}
    sorted_recommendations: list[tuple[float, str]] = sorted(revesed_recommendations.items(), reverse=False)
    return [ sorted_recommendations[i][1] for i in range(n_recommendations) ]

# Run cafe recommendations for all users.
def _run_cafe_recommendations() -> Dict[str, List[str]]:
    users: list[User] = DButils.get_all_users()
    all_cafe: list[Cafe] = DButils.get_all_cafe()
    recommendations: dict[str, list[str]] = {}
    try:
        for _, user in enumerate( tqdm(users, desc="Finding cafe recommendations") ):
            user_recommendations = []
            if user['first_name'] == "Tom":
                content_based_recs: dict[str, float] = content_based.main(all_cafe=all_cafe, user=user)
                collab_based_recs: dict[str, float] = collaborative.main(users=users, user=user)

                scored_recommendations: dict[str, float] = assign_final_scores(content_based_recs, collab_based_recs)

                user_recommendations: list[str] = sort_cafe_recommendations(scored_recommendations)

                # user_recommendations.extend(content_based_recs)
                # user_recommendations.extend(collab_based_recs)

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