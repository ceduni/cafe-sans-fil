### Algorithme 4.4 ###
from datetime import datetime
from app.models.cafe_model import Cafe, MenuItem
import recommender_systems.utils.utilitaries as Utilitaries
from app.models.order_model import Order, OrderedItem
from app.services.order_service import OrderService
from app.services.cafe_service import CafeService
from typing import List, Any

# Recommand foods to all the users based on the time and the most bought/liked
#   foods.
#TODO: Recommand items based on the time of the day. 
#   Should be done after nutritionist advice.
async def main(cafe: Cafe) -> List[str]:
    time_of_the_day: Any #TODO
    cafe_items: list[MenuItem] = cafe.menu_items
    filters = {
        "page": 1,
        "limit": 20,
        "sort_by": "-order_number"
    }
    all_orders: List[Order] = OrderService.list_orders(**filters)

    # Number of items to recommand.
    if len(cafe_items) > 50:
        k: int = len(cafe_items)//2
    else:
        k: int = len(cafe_items)

    # Most bought items
    items: List[str] = Utilitaries.most_bought_items(all_orders)

    menu_items: List[MenuItem] = []
    for item_slug in items:
        menu_items.append( await CafeService.retrieve_menu_item(cafe.slug, item_slug) )

    items_choice: List[MenuItem] = Utilitaries.most_liked_items(menu_items, k)

    return Utilitaries.items_slugs(items_choice)
