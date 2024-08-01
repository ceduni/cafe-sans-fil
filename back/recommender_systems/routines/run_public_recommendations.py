from recommender_systems.systems.items_recommenders import global_recommendation as GR
from app.models.cafe_model import Cafe
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
from typing import List, Dict
from recommender_systems.utils.api_calls import RecommendationsApi, AuthApi
from tqdm import tqdm
import time

# Dictionnary recommendations structure:
# {
#   "cafe_slug": [
#          item_slug,
#    ],
# }
def _run_public_recommendations() -> Dict[str, List[str]]:
    all_cafe: list[Cafe] = DButils.get_all_cafe()
    public_recommendations: dict[str, list[str]] = {}
    for _, cafe in enumerate(tqdm(all_cafe, desc="Finding public recommendations")):
        cafe_slug = cafe['slug']
        # if cafe_slug in ["acquis-de-droit"]:
        if cafe_slug not in public_recommendations:
            public_recommendations[cafe_slug] = []
        public_recommendations[cafe_slug].extend( Utilitaries.filter_items_by_cafe(GR.main(cafe), cafe_slug) )
    return public_recommendations

def update_public_recommendations() -> None:
    auth_token = AuthApi.auth_login()
    recommendations: dict[str, list[str]] = _run_public_recommendations()
    for _, cafe_slug in enumerate(tqdm(recommendations.keys(), desc="Updating public recommendations")):
        _, status = RecommendationsApi.get_cafe(cafe_slug=cafe_slug)

        if status != 200:
            data = {
                "health_score": 100,
                "public_recommendations": recommendations[cafe_slug],
            }
        else:
            data = {
                "public_recommendations": recommendations[cafe_slug],
            }

        RecommendationsApi.update_public_recommendations(auth_token=auth_token, cafe_slug=cafe_slug, json_data=data)
