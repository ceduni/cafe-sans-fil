# Ce fichier contient le code des algorithmes de la section 2 du document
#   "Logique" du wiki.
from typing import List, Union
from back.app.models.cafe_model import MenuItem, Cafe
from back.app.models.user_model import User
from back.app.models.order_model import Order, OrderedItem
from back.app.services.cafe_service import CafeService
from back.app.services.order_service import OrderService
from back.app.services.user_service import UserService
import uuid

# Takes a list of items as parameter and returns a list that contains the slugs
#   of the items.
def items_slugs(items: List[MenuItem]) -> List[str]:
    return list(map(lambda x: x.slug, items))

# This method takes a list of orders ids and return a list of all the items
#   contained in these orders.
async def list_items(orders_ids: List[str], action: str) -> Union[List[MenuItem], List[str]]:
    items: list[MenuItem] = []
    all_slugs: list[str] = []
    for id in orders_ids:
        order: Order = await OrderService.retrieve_order(uuid.UUID(id))
        cafe_slug: str = order.cafe_slug
        ordered_items: list[OrderedItem] = order.items     
        slugs: list[str] = []       
        for item in ordered_items:
            slugs.append(item.item_slug)
        all_slugs.extend(slugs)
        items.extend(await get_items_from_slugs(slugs, cafe_slug))
            
    if action == "slugs":
        return all_slugs
    elif action == "items":
        return items

async def get_items_from_slugs(slugs: List[str], cafe_slug: str) -> List[MenuItem]:
    items: list[MenuItem] = []
    for slug in slugs:
        retrived_item: MenuItem = await CafeService.retrieve_menu_item(cafe_slug, slug)
        if retrived_item not in items:
            items.append(retrived_item) if retrived_item != None else None
    return items

# This method takes the actual user and the cafe as parameters and return
#   a list of items not yet consummed by the user.
async def meal_not_consumed(cafe: Cafe, user: User) -> List[MenuItem]:
    cafe_slug = cafe.slug
    order_history: list[Order] = user.order_history
    oredered_items_slugs: list[str] = []
    for order in order_history:
        oredered_items: list[OrderedItem] = order.items
        for item in oredered_items:
            oredered_items_slugs.append(item.item_slug)
    
    meal_not_consumed: list[MenuItem] = []
    for item_slug in oredered_items_slugs:
        item = await CafeService.retrieve_menu_item(cafe_slug, item_slug)
        if item != None:
            meal_not_consumed.append(item)

    return meal_not_consumed

# Get all items
async def get_all_items() -> List[MenuItem]:
    query_params = {
        "cafe_id_or_slug": None,
        "page": 1,
        "limit": 40,
        "sort_by": "nothing"
    }
    items: list[MenuItem] = await CafeService.list_menu_items(**query_params)
    return items

# Get all cafe
async def get_all_cafe() -> List[Cafe]:
    query_params = {
        "page": 1,
        "limit": 40,
        "sort_by": "name"
    }
    cafes: list[Cafe] = await CafeService.list_cafes(**query_params)
    return cafes

#TODO: Get a user list instead of a dictionnary.
async def get_all_users() -> List[User]:
    filters = {
        "page": 1,
        "limit": 20,
        "sort_by": "last_name"
    }
    users: list[User] = await UserService.list_users(**filters)
    return users