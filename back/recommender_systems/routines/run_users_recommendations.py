from recommender_systems.systems import collaborative_filtering as CF
from recommender_systems.systems import content_based_filtering as CBF
from recommender_systems.systems import knowledge_based as KBR
from app.models.user_model import User
from app.models.cafe_model import Cafe
from app.schemas.recommendation_schema import RecommendationUpdate
from app.services.recommendation_service import RecommendationService
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
import asyncio
from typing import List, Dict

#TODO
# Find the recommendations for all users.
async def _run_users_recommendations() -> Dict[str, Dict[str, List[str]]]:
    users: list[User] = asyncio.run(DButils.get_all_users())
    list_cafe: list[Cafe] = asyncio.run(DButils.get_all_cafe())
    recommendations: dict[str, dict[str, list[str]]] = {}
    for user in users:
        if user.id not in recommendations:
            cafes: dict[str, list[str]] = {}
            cf_recommendations: list[str] = CF.main(users, user)
            for cafe in list_cafe:
                cafe_slug: str = cafe.slug
                # Personnal recommendations.
                collab_filtering: list[str] = await Utilitaries.filter_items_by_cafe(cf_recommendations, cafe_slug)
                content_based: list[str] = await Utilitaries.filter_items_by_cafe(CBF.main(user, cafe), cafe_slug)
                knowledge_based: list[str] = await Utilitaries.filter_items_by_cafe(KBR.main(cafe, user), cafe_slug)

                if cafe_slug not in cafes:
                    cafes[cafe_slug] = []

                cafes[cafe_slug].extend(collab_filtering)
                cafes[cafe_slug].extend(content_based)
                cafes[cafe_slug].extend(knowledge_based)
            
            recommendations[user.id] = cafes

    
    #TODO Define a proportion ofr recommendations.

    return recommendations

# Update recommendations for each user in the database.
def update_users_recommendations() -> None:
    recommendations: dict[str, dict[str, list[str]]] = asyncio.run(_run_users_recommendations())
    for user_id in recommendations.keys():
        for cafe_slug in recommendations[user_id]:
            data = {
                "recommendations": recommendations[user_id][cafe_slug]
            }
            asyncio.run( RecommendationService.update_user_recommendations(user_id, cafe_slug, RecommendationUpdate(**data)) )
