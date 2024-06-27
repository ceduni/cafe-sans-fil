# Ce fichier contient le code des algorithmes de la section 2 du document
#   "Logique" du wiki.
from typing import List, Any, Tuple
from app.models.cafe_model import MenuItem, Cafe
from app.models.user_model import User
from app.models.order_model import Order, OrderedItem
from app.services.cafe_service import CafeService
from app.services.order_service import OrderService
from app.services.user_service import UserService
from collections import Counter
from typing import List, Dict
import uuid

def regroup_by_cluster(items: List[MenuItem]) -> Dict[str, List[MenuItem]]:
    groups: dict[str, list[MenuItem]] = {}
    for item in items:
        if item.cluster not in groups:
            groups[item.cluster] = []
        groups[item.cluster].append(item)
    return groups
    

# Check if a values is duplicated in a list.
def is_duplicated(element: Any, list: List[Any]) -> bool:
    counts = Counter(list)
    return counts[element] > 1

#TODO
def health_score():
    pass

def reshape(A: List[Any], B: List[Any]) -> Tuple[List[Any]]:
    if len(A) == len(B):
        return (A, B)
    elif len(A) < len(B):
        for _ in range(len(B) - len(A)):
            A.append('0')
        return (A, B)
    else:
        for _ in range(len(A) - len(B)):
            B.append('0')
        return (A, B)    

# Takes a list of items as parameter and returns a list that contains the slugs
#   of the items.
def items_slugs(items: List[MenuItem]) -> List[str]:
    return list(map(lambda x: x.slug, items))

# This method takes a list of orders ids and return a list of all the items
#   (slugs of the items) contained in these orders.
async def list_items(orders_ids: List[str]) -> List[str]:
    all_slugs: list[str] = []
    for id in orders_ids:
        order: Order = await OrderService.retrieve_order(uuid.UUID(id))
        ordered_items: list[OrderedItem] = order.items     
        slugs: list[str] = []       
        for item in ordered_items:
            slugs.append(item.item_slug)
        all_slugs.extend(slugs)
    return all_slugs

# Takes a list of item slugs and a cafe slug and returns a list of slugs of
#   items sold in this cafe.
async def filter_items_by_cafe(slugs: List[str], cafe_slug: str) -> List[str]:
    items: list[str] = []
    for slug in slugs:
        retrived_item: MenuItem = await CafeService.retrieve_menu_item(cafe_slug, slug)
        if retrived_item != None:
            items.append(retrived_item.slug) if retrived_item.slug not in items else None
    return items

# This method takes a user and a cafe as parameters and return
#   a list of items not yet bought by the user in this cafe.
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
