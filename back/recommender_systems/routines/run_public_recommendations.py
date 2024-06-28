from recommender_systems.systems.items_recommenders import global_recommendation as GR
from app.models.cafe_model import Cafe
from app.services.recommendation_service import RecommendationService
from app.schemas.recommendation_schema import ItemRecommendationUpdate
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
import asyncio
from typing import List, Dict

# Dictionnary recommendations structure:
# {
#   "cafe_slug": [
#          item_slug,
#    ],
# }
async def _run_public_recommendations() -> Dict[str, List[str]]:
    all_cafe: list[Cafe] = await DButils.get_all_cafe()
    public_recommendations: dict[str, list[str]] = {}
    for cafe in all_cafe:
        cafe_slug = cafe.slug
        if cafe_slug not in public_recommendations:
            public_recommendations[cafe_slug] = []
        public_recommendations[cafe_slug].extend( await Utilitaries.filter_items_by_cafe(GR.main(cafe)), cafe_slug )
    return public_recommendations

def update_public_recommendations() -> None:
    recommendations: dict[str, list[str]] = asyncio.run( _run_public_recommendations() )
    for cafe_slug in recommendations.keys():
        data = {
            "recommendations": recommendations[cafe_slug]
        }
        asyncio.run( RecommendationService.update_public_recommendations(cafe_slug, ItemRecommendationUpdate(**data)) )