from recommender_systems.utils import db_utils as DButils, utilitaries as Utils
from recommender_systems.utils.api_calls import RecommendationsApi, AuthApi, CafeApi
from tqdm import tqdm

def update_cafes_health_score() -> None:
    auth_token = AuthApi.auth_login()
    all_cafes = DButils.get_all_cafe()
    for _, cafe in enumerate(tqdm(all_cafes, desc="Updating cafe health score")):
        cafe_score: float = Utils.calculate_cafe_health_score(cafe)
        _, status = RecommendationsApi.get_cafe(cafe_slug=cafe["slug"])
        
        if status != 200:
            data = {
                "health_score": cafe_score,
                "public_recommendations": [],
            }
        else:
            data = {
                "health_score": cafe_score
            }
        CafeApi.update_cafe(auth_token=auth_token, cafe_slug=cafe['slug'], json_data=data)
        RecommendationsApi.update_cafe_health_score(auth_token=auth_token, cafe_slug=cafe['slug'], json_data=data)
