from app.models.cafe_model import Cafe
from recommender_systems.utils import utilitaries as Utils
from typing import List, Dict
from app.services.cafe_service import CafeService

async def run_bot_recommendations(cafe_slug: str) -> List[str]:
    cafe = await CafeService.retrieve_cafe(cafe_id_or_slug=cafe_slug)
    recommendations = Utils.sort_by_health_score_for_objects(cafe.menu_items)
    return recommendations
