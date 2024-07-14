from recommender_systems.systems.items_recommenders import health_bot as HB
from app.models.cafe_model import Cafe
from recommender_systems.utils import db_utils as DButils
from typing import List, Dict
from recommender_systems.utils.api_calls import BotRecommenderApi, AuthApi
from tqdm import tqdm
import time

# Dictionnary recommendations structure:
# {
#   "cafe_slug": [
#          item_slug,
#    ],
# }
def _run_bot_recommendations() -> Dict[str, List[str]]:
    all_cafe: list[Cafe] = DButils.get_all_cafe()
    bot_recommendations: dict[str, list[str]] = HB.main(all_cafe)
    return bot_recommendations

# Update bot's recommendations in the database
def update_bot_recommendations() -> None:
    auth_token = AuthApi.auth_login()
    recommendations: dict[str, list[str]] = _run_bot_recommendations()
    for _, cafe_slug in enumerate( tqdm(recommendations, desc="Updating bot recommendations") ):
        data = {
            "recommendations": recommendations[cafe_slug]
        }
        response, status = BotRecommenderApi.update_bot_recommendations(auth_token=auth_token, cafe_slug=cafe_slug, json_data=data)
        print(response, status)
