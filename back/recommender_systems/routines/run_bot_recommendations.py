from recommender_systems.systems.items_recommenders import health_bot as HB
from app.models.user_model import User
from app.models.cafe_model import Cafe
from app.schemas.recommendation_schema import ItemRecommendationUpdate
from app.services.recommendation_service import RecommendationService
from recommender_systems.utils import db_utils as DButils
from typing import List, Dict
import asyncio

# Dictionnary recommendations structure:
# {
#   "cafe_slug": [
#          item_slug,
#    ],
# }
async def _run_bot_recommendations() -> Dict[str, List[str]]:
    all_cafe: list[Cafe] = await DButils.get_all_cafe()
    bot_recommendations: dict[str, list[str]] = HB.main(all_cafe)
    return bot_recommendations

# Update bot's recommendations in the database
def update_bot_recommendations() -> None:
    recommendations: dict[str, list[str]] = asyncio.run( _run_bot_recommendations() )
    for cafe_slug in recommendations:
        data = {
            "recommendations": recommendations[cafe_slug]
        }
        asyncio.run( RecommendationService.update_bot_recommendations(cafe_slug, ItemRecommendationUpdate(**data)) )
