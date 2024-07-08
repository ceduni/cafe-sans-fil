from recommender_systems.systems.items_recommenders import global_recommendation as GR
from app.models.cafe_model import Cafe
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
from typing import List, Dict
from recommender_systems.utils.api_calls import PublicRecommenderApi, AuthApi
from tqdm import tqdm

# Dictionnary recommendations structure:
# {
#   "cafe_slug": [
#          item_slug,
#    ],
# }
def _run_public_recommendations() -> Dict[str, List[str]]:
    all_cafe: list[Cafe] = DButils.get_all_cafe()
    public_recommendations: dict[str, list[str]] = {}
    for _, cafe in enumerate(tqdm(all_cafe, desc="Running public recommendations")):
        cafe_slug = cafe['slug']
        if cafe_slug not in public_recommendations:
            public_recommendations[cafe_slug] = []
        public_recommendations[cafe_slug].extend( Utilitaries.filter_items_by_cafe(GR.main(cafe), cafe_slug) )
    return public_recommendations

def update_public_recommendations() -> None:
    auth_token = AuthApi.auth_login()
    recommendations: dict[str, list[str]] = _run_public_recommendations()
    print(recommendations)
    for _, cafe_slug in enumerate(tqdm(recommendations.keys(), desc="Updating public recommendations")):
        data = {
            "recommendations": recommendations[cafe_slug]
        }
        PublicRecommenderApi.update_public_recommendations(auth_token=auth_token, cafe_slug=cafe_slug, json_data=data)
