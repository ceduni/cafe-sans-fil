from recommender_systems.utils import db_utils as DButils, utilitaries as Utilitaries
from app.services.cafe_service import CafeService
from app.models.cafe_model import MenuItem, Cafe
from app.schemas.cafe_schema import MenuItemUpdate
import asyncio

def update_items_health_score() -> None:
    all_cafe: list[Cafe] = asyncio.run( DButils.get_all_cafe() )
    for cafe in all_cafe:
        cafe_slug = cafe.slug
        items: list[MenuItem] = cafe.menu_items
        for item in items:
            score: str = Utilitaries.health_score(item)
            item_data = {
                "health_score": score
            }
            asyncio.run( CafeService.update_menu_item(cafe_slug, item.slug, MenuItemUpdate(**item_data)) )
            