from recommender_systems.utils import db_utils as DButils, utilitaries as Utilitaries
from app.models.cafe_model import MenuItem, Cafe
from recommender_systems.utils.api_calls import CafeApi, AuthApi
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
                item_data = {
                    "health_score": score
                }
                CafeApi.update_item(auth_token=auth_token, cafe_slug=cafe['slug'], item_slug=item['slug'], json_data=item_data)
    except KeyError | TypeError as e:
        print(e)