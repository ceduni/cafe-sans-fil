### Algorithme 4.4 ###
from app.models.cafe_model import Cafe, MenuItem
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
from app.models.order_model import Order
from typing import List, Any

# Recommand foods to all the users based on the time and the most bought/liked
#   foods.
#TODO: Recommand items based on the time of the day. 
#   Should be done after nutritionist advice.
def main(cafe: Cafe) -> List[str]:
    time_of_the_day: Any #TODO
    cafe_items: list[MenuItem] = DButils.get_cafe_items(cafe['slug'])
    # filters = {
    #     "page": 1,
    #     "limit": 20,
    #     "sort_by": "-order_number"
    # }

    if len(cafe_items) == 0:
        return []
    
    all_orders: List[Order] = DButils.get_all_orders()


    # Number of items to recommand.
    if len(cafe_items) > 50:
        k: int = len(cafe_items)//2
    else:
        k: int = len(cafe_items)

    # Most bought items
    items: List[str] = Utilitaries.most_bought_items(all_orders)

    menu_items: List[MenuItem] = []
    for item_slug in items:
        menu_items.append( DButils.get_item(cafe['slug'], item_slug) )

    items_choice: List[str] = Utilitaries.most_liked_items(menu_items, k)

    return items_choice
