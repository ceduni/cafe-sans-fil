from recommender_systems.systems.items_recommenders import collaborative_filtering as CF
from recommender_systems.systems.items_recommenders import content_based_filtering as CBF
from recommender_systems.systems.items_recommenders import knowledge_based as KBR
from app.models.user_model import User
from app.models.cafe_model import Cafe, MenuItem
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
from typing import List, Dict
from recommender_systems.utils.api_calls import RecommendationsApi, AuthApi
from tqdm import tqdm
import random


def _run_users_recommendations() -> Dict[str, Dict[str, List[str]]]:
    users: list[User] = DButils.get_all_users()
    list_cafe: list[Cafe] = DButils.get_all_cafe()
    recommendations: dict[str, dict[str, list[str]]] = {}
    for _, user in enumerate(tqdm(users, desc="Finding users recommendations")):
        if user['username'] not in recommendations and user['username'] == '7802085':
            cafes_recommendations: dict[str, list[str]] = {}
            # cf_recommendations: list[str] = CF.main(users, user)
            for cafe in list_cafe:
                cafe_slug: str = cafe['slug']
                # Personnal recommendations.
                # collab_filtering: list[str] = cf_recommendations
                content_based: dict[str, int] = CBF.main(user, cafe)
                knowledge_based: dict[str, int] = KBR.main(cafe, user)

                if cafe_slug not in cafes_recommendations:
                    cafes_recommendations[cafe_slug] = []

                list_items_recommended: list[dict[str, int]] = []

                # list_items_recommended.extend(collab_filtering)
                list_items_recommended.append(content_based)
                list_items_recommended.append(knowledge_based)

                # print("content_based", content_based)
                # print("knowledge_based", knowledge_based)

                cafes_recommendations[cafe_slug] = _final_reommendations(list_items_recommended)
            
            recommendations[user['username']] = cafes_recommendations

    #TODO Define a proportion ofr recommendations.

    # sorted_recommendations: dict[str, dict[str, list[str]]] = _sort_recommendations(recommendations)

    # return sorted_recommendations
    return recommendations
    
def _final_reommendations(itemsScored: List[Dict[str, int]]) -> List[str]:
    items_slug: list[str] = []
    #print(itemsScored)
    for recommendation in itemsScored:
        items_slug.extend(list(recommendation.keys()))

    items_tuples: list[tuple[int, str]] = []
    for item in items_slug:
        if item not in items_tuples:
            if item not in itemsScored[0]:
                itemsScored[0][item] = 0
            if item not in itemsScored[1]:
                itemsScored[1][item] = 0
            
            score_1 = itemsScored[0][item]
            score_2 = itemsScored[1][item]

            items_tuples.append( ( (score_1 + score_2), item ) )
        
    sorted_items_tuples: list[tuple[int, str]] = sorted(items_tuples, reverse=True)

    sorted_items: List[str] = []
    for item_tuple in sorted_items_tuples:
        sorted_items.append(item_tuple[1])

    return sorted_items


# Update recommendations for each user in the database.
def update_users_recommendations() -> None:
    auth_token = AuthApi.auth_login()
    recommendations: dict[str, dict[str, list[str]]] = _run_users_recommendations()
    all_bot_recommendations = {}
    if recommendations != {}:
        for _, username in enumerate( tqdm(recommendations.keys(), desc="Updating users recommendations") ):
            user = DButils.get_user(username=username)
            _, status = RecommendationsApi.get_user(user_id=user["user_id"])
            personnal_recommendations: list[dict[str, list[str]]] = []
            for cafe_slug in recommendations[username]:
                if cafe_slug not in all_bot_recommendations:
                    bot_recommendations, _ = RecommendationsApi.get_bot_recommendations(cafe_slug=cafe_slug)
                    all_bot_recommendations[cafe_slug] = bot_recommendations

                bot_recommendations = all_bot_recommendations[cafe_slug]
                
                merged_recommendation = []
                merged_recommendation.extend(recommendations[username][cafe_slug])
                merged_recommendation.extend(bot_recommendations)
                merged_recommendation = list( set(merged_recommendation) )

                random.shuffle( merged_recommendation )
                final_recommendation = random.sample(merged_recommendation, 6)

                personnal_recommendations.append(
                    {
                        "cafe_slug": cafe_slug,
                        "recommendation": final_recommendation
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