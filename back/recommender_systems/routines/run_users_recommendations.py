from recommender_systems.systems.items_recommenders import collaborative_filtering as CF
from recommender_systems.systems.items_recommenders import content_based_filtering as CBF
from recommender_systems.systems.items_recommenders import knowledge_based as KBR
from app.models.user_model import User
from app.models.cafe_model import Cafe, MenuItem
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
from typing import List, Dict
from recommender_systems.utils.api_calls import UserRecommenderApi, AuthApi
from tqdm import tqdm
import time

#TODO
# Find the recommendations for all users.
# Dictionnary recommendations structure:
# {
#   "user_id": {
#          "cafe_slug": ["item_id",],
#    },
# }
def _run_users_recommendations() -> Dict[str, Dict[str, List[str]]]:
    users: list[User] = DButils.get_all_users()
    list_cafe: list[Cafe] = DButils.get_all_cafe()
    recommendations: dict[str, dict[str, list[str]]] = {}
    for _, user in enumerate(tqdm(users, desc="Finding users recommendations")):
        if user['user_id'] not in recommendations and user['username'] == '7802085':
            cafes_recommendations: dict[str, list[str]] = {}
            #cf_recommendations: list[str] = CF.main(users, user)
            for cafe in list_cafe:
                cafe_slug: str = cafe['slug']
                # Personnal recommendations.
                # collab_filtering: list[str] = Utilitaries.filter_items_by_cafe(cf_recommendations, cafe_slug)
                
                # try:
                #     content_based: list[str] = Utilitaries.filter_items_by_cafe(CBF.main(user, cafe), cafe_slug)
                # except ValueError:
                #     print(f"Error for user: {user['username']} in content based algorithm.")
                #     content_based: list[str] = []

                try:
                    knowledge_based: list[str] = Utilitaries.filter_items_by_cafe(KBR.main(cafe, user), cafe_slug)
                    print("knowledge_based:", knowledge_based) if len(knowledge_based) < 20 else None
                except KeyError | ValueError:
                    print(f"Error for user: {user['username']} in knowledge based algorithm.")
                    knowledge_based: list[str] = []

                if cafe_slug not in cafes_recommendations:
                    cafes_recommendations[cafe_slug] = []

                list_items_recommended = []

                # list_items_recommended.extend(collab_filtering)
                # list_items_recommended.extend(content_based)
                list_items_recommended.extend(knowledge_based)

                cafes_recommendations[cafe_slug] = list( set(list_items_recommended) )
            
            recommendations[user['user_id']] = cafes_recommendations

    #TODO Define a proportion ofr recommendations.

    sorted_recommendations: dict[str, dict[str, list[str]]] = _sort_recommendations(recommendations)

    return sorted_recommendations
    
def _sort_recommendations(recommendations: Dict[str, Dict[str, List[str]]]) -> Dict[str, Dict[str, List[str]]]:
    sorted_recommendations: dict[str, dict[str, list[str]]] = {}
    for _, user in enumerate(tqdm(recommendations.keys(), desc="Sorting recommendations")):
        cafes_sorted: dict[str, list[str]] = {}
        for cafe_slug in recommendations[user].keys():
            items: list[MenuItem] = []
            for item_slug in recommendations[user][cafe_slug]:
                items.append( DButils.get_item(cafe_slug, item_slug) )
            cafes_sorted[cafe_slug] = Utilitaries.sort_by_health_score(items)

        sorted_recommendations[user] = cafes_sorted

    return sorted_recommendations

# Update recommendations for each user in the database.
def update_users_recommendations() -> None:
    auth_token = AuthApi.auth_login()
    recommendations: dict[str, dict[str, list[str]]] = _run_users_recommendations()
    # if recommendations != {}:
    #     for _, user_id in enumerate( tqdm(recommendations.keys(), desc="Updating users recommendations") ):
    #         for cafe_slug in recommendations[user_id]:
    #             data = {
    #                 "recommendations": recommendations[user_id][cafe_slug]
    #             }
    #             UserRecommenderApi.update_user_recommendations(auth_token=auth_token, user_id=user_id, cafe_slug=cafe_slug,json_data=data)
