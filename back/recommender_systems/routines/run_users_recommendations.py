from recommender_systems.systems.items_recommenders import collaborative_filtering as CF
from recommender_systems.systems.items_recommenders import content_based_filtering as CBF
from recommender_systems.systems.items_recommenders import knowledge_based as KBR
from app.models.user_model import User
from app.models.cafe_model import Cafe, MenuItem
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
from typing import List, Dict
from recommender_systems.utils.api_calls import RecommendationsApi, AuthApi
from tqdm import tqdm
import time


def _run_users_recommendations() -> Dict[str, Dict[str, List[str]]]:
    users: list[User] = DButils.get_all_users()
    list_cafe: list[Cafe] = DButils.get_all_cafe()
    recommendations: dict[str, dict[str, list[str]]] = {}
    for _, user in enumerate(tqdm(users, desc="Finding users recommendations")):
        if user['username'] not in recommendations and user['username'] == '7802085':
            cafes_recommendations: dict[str, list[str]] = {}
            cf_recommendations: list[str] = CF.main(users, user)
            for cafe in list_cafe:
                cafe_slug: str = cafe['slug']
                # Personnal recommendations.
                collab_filtering: list[str] = Utilitaries.filter_items_by_cafe(cf_recommendations, cafe_slug)
                content_based: list[str] = Utilitaries.filter_items_by_cafe(CBF.main(user, cafe), cafe_slug)
                knowledge_based: list[str] = Utilitaries.filter_items_by_cafe(KBR.main(cafe, user), cafe_slug)

                if cafe_slug not in cafes_recommendations:
                    cafes_recommendations[cafe_slug] = []

                list_items_recommended = []

                list_items_recommended.extend(collab_filtering)
                list_items_recommended.extend(content_based)
                list_items_recommended.extend(knowledge_based)

                cafes_recommendations[cafe_slug] = list( set(list_items_recommended) )
            
            recommendations[user['username']] = cafes_recommendations

    #TODO Define a proportion ofr recommendations.

    # sorted_recommendations: dict[str, dict[str, list[str]]] = _sort_recommendations(recommendations)

    # return sorted_recommendations
    return recommendations
    
# def _sort_recommendations(recommendations: Dict[str, Dict[str, List[str]]]) -> Dict[str, Dict[str, List[str]]]:
#     sorted_recommendations: dict[str, dict[str, list[str]]] = {}
#     for _, user in enumerate(tqdm(recommendations.keys(), desc="Sorting recommendations")):
#         cafes_sorted: dict[str, list[str]] = {}
#         for cafe_slug in recommendations[user].keys():
#             items: list[MenuItem] = []
#             for item_slug in recommendations[user][cafe_slug]:
#                 items.append( DButils.get_item(cafe_slug, item_slug) )
#             cafes_sorted[cafe_slug] = Utilitaries.sort_by_health_score(items)

#         sorted_recommendations[user] = cafes_sorted

#     return sorted_recommendations

# Update recommendations for each user in the database.
def update_users_recommendations() -> None:
    auth_token = AuthApi.auth_login()
    recommendations: dict[str, dict[str, list[str]]] = _run_users_recommendations()
    if recommendations != {}:
        for _, username in enumerate( tqdm(recommendations.keys(), desc="Updating users recommendations") ):
            user = DButils.get_user(username=username)
            _, status = RecommendationsApi.get_user(user_id=user["user_id"])
            personnal_recommendations: list[dict[str, list[str]]] = []
            for cafe_slug in recommendations[username]:
                personnal_recommendations.append(
                    {
                        "cafe_slug": cafe_slug,
                        "recommendation": recommendations[username][cafe_slug]
                    }
                )

            if status != 200:
                data = {
                    "user_id": user['user_id'],
                    "username": username,
                    "personnal_recommendations": personnal_recommendations,
                    "cafe_recommendations": [],
                }
            else:
                data = {
                    "personnal_recommendations": personnal_recommendations
                }
            
            RecommendationsApi.update_user_personnal_recommendations(auth_token=auth_token, user_id=user["user_id"], json_data=data)