from recommender_systems.systems.cafe_recommenders import collaborative
from recommender_systems.systems.cafe_recommenders import content_based
from app.models.user_model import User
from app.models.cafe_model import Cafe
from app.schemas.recommendation_schema import CafeRecommendationUpdate
from app.services.recommendation_service import RecommendationService
from recommender_systems.utils import db_utils as DButils
from typing import List, Dict
import asyncio

async def _run_cafe_recommendations() -> Dict[str, List[str]]:
    users: list[User] = asyncio.run(DButils.get_all_users())
    all_cafe: list[Cafe] = asyncio.run(DButils.get_all_cafe())
    recommendations: dict[str, list[str]] = {}
    for user in users:
        recommendations[user.id] = collaborative.main(users, user).extend( content_based.main(all_cafe, user) )
    return recommendations

# Update cafe recommendations for all users.
def update_cafe_recommendations():
    recommendations: dict[str, list[str]] = asyncio.run( _run_cafe_recommendations() )
    for user_id in recommendations.keys():
        data = {
            "recommendations": recommendations[user_id]
        }
        asyncio.run( RecommendationService.update_user_cafe_recommendations(user_id, CafeRecommendationUpdate(**data)) )