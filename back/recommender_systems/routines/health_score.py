from recommender_systems.utils import db_utils as DButils, utilitaries as Utilitaries
from app.models.cafe_model import MenuItem, Cafe
from recommender_systems.utils.api_calls import RecommendationsApi, AuthApi
from tqdm import tqdm

# Update the health score of each item in the database.
def update_items_health_score() -> None:
    auth_token = AuthApi.auth_login()
    all_cafe: list[Cafe] = DButils.get_all_cafe()
    try:
        for _, cafe in enumerate( tqdm(all_cafe, desc="Updating items health score") ):
            cafe_slug = cafe['slug']
            items: list[MenuItem] = DButils.get_cafe_items(cafe_slug)
            for item in items:
                score: float = Utilitaries.health_score(item)
                _, status = RecommendationsApi.get_item(item_id=item['item_id'])
                if status != 200:
                    item_data = {
                        "item_id": item['item_id'],
                        "slug": item['slug'],
                        "health_score": score,
                        "cluster": "unclustered"
                    }
                else:
                    item_data = {
                        "health_score": score
                    }
                RecommendationsApi.update_items_health_score(auth_token=auth_token, item_id=item['item_id'], json_data=item_data)

    except (KeyError, TypeError) as e:
        print(e)