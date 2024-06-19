# Ce fichier contient le code des algorithmes de la section 2 du document
#   "Logique" du wiki.
from typing import List, Union
from back.app.models.cafe_model import MenuItem, Cafe
from back.app.models.user_model import User
from back.app.models.order_model import Order, OrderedItem
from back.app.services.cafe_service import CafeService
from back.app.services.order_service import OrderService
import uuid

# Takes a list of items as parameter and returns a list that contains the ids
#   of the items.
def items_ids(items: List[MenuItem]) -> List[str]:
    return list(map(lambda x: x.item_id, items))

# This method takes a list of orders ids and return a list of all the items
#   contained in these orders.
async def list_items(orders_ids: List[str], action: str) -> Union[List[MenuItem], List[str]]:
    items: list[MenuItem] = []
    for id in orders_ids:
        order: Order = await OrderService.retrieve_order(uuid.UUID(id))
        cafe_slug: str = order.cafe_slug
        ordered_items: list[OrderedItem] = order.items            
        for item in ordered_items:
            retrived_item = await CafeService.retrieve_menu_item(cafe_slug, item.item_slug)
            items.append(retrived_item) if retrived_item != None else None
            
    if action == "ids":
        return items_ids(items)
    elif action == "items":
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

'''
def intersection(A: list, B: list) -> list:
    res = []
    for elem in A:
        if elem in B:
            res.append(elem)
    return res

### Test the code with each similarity and choose the best one.
def jaccard(A: list, B: list):
    A.extend(B)
    inter = intersection(A, B)
    return len(inter) / len(A)

def cosine_similarity(x,y):
    return

def pearson_correlation(x,y):
    return
'''
