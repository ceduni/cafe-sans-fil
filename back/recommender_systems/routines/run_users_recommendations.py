from recommender_systems.systems.items_recommenders import collaborative_filtering as CF
from recommender_systems.systems.items_recommenders import content_based_filtering as CBF
from recommender_systems.systems.items_recommenders import knowledge_based as KBR
from app.models.user_model import User
from app.models.cafe_model import Cafe
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
    try:
        for _, user in enumerate(tqdm(users, desc="Running users recommendations")):
            if user['user_id'] not in recommendations:
                cafes: dict[str, list[str]] = {}
                cf_recommendations: list[str] = CF.main(users, user)
                for cafe in list_cafe:
                    cafe_slug: str = cafe['slug']
                    # Personnal recommendations.
                    collab_filtering: list[str] = Utilitaries.filter_items_by_cafe(cf_recommendations, cafe_slug)
                    content_based: list[str] = Utilitaries.filter_items_by_cafe(CBF.main(user, cafe), cafe_slug)
                    knowledge_based: list[str] = Utilitaries.filter_items_by_cafe(KBR.main(cafe, user), cafe_slug)

                    if cafe_slug not in cafes:
                        cafes[cafe_slug] = []

                    cafes[cafe_slug].extend(collab_filtering)
                    cafes[cafe_slug].extend(content_based)
                    cafes[cafe_slug].extend(knowledge_based)
                
                recommendations[user['user_id']] = cafes

        #TODO Define a proportion ofr recommendations.

        return recommendations

    except ValueError as e:
        print(e)
        return {}

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
