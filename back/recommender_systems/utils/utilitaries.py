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

# Take a list of cafe and an item and return a list of cafe selling the item.
def find_cafe_by_item(cafe_list: List[Cafe], item: MenuItem) -> List[Cafe]:
    return [ cafe for cafe in cafe_list if item in cafe.menu_items ]

def find_indices(input_list, value):
    return [i for i, x in enumerate(input_list) if x == value]

def regroup_by_cluster(items: List[MenuItem]) -> Dict[str, List[MenuItem]]:
    groups: dict[str, list[MenuItem]] = {}
    for item in items:
        if item.cluster not in groups:
            groups[item.cluster] = []
        groups[item.cluster].append(item)
    return groups
    
# Calculate the nutriscore of an item
def health_score(item: MenuItem) -> str:
    nutri_info: dict[str, float] = item.nutritional_informations

    # Negative points
    energy_points = min(max(int(nutri_info["energy"] / 335), 0), 10)
    sugar_points = min(max(int(nutri_info["sugars"] / 4.5), 0), 10)
    saturated_fat_points = min(max(int(nutri_info["saturated_fat"] / 1), 0), 10)
    sodium_points = min(max(int(nutri_info["sodium"] / 90), 0), 10)
    negative_points = energy_points + sugar_points + saturated_fat_points + sodium_points

    # Positive points
    fiber_points = min(max(int(nutri_info["fiber"] / 0.9), 0), 5)
    protein_points = min(max(int(nutri_info["protein"] / 1.6), 0), 5)
    if nutri_info["percentage_fruit_vegetables_nuts"]:
        fruit_vegetables_nuts_points = min(max(int(nutri_info["percentage_fruit_vegetables_nuts"] / 40), 0), 5)
        positive_points = fiber_points + protein_points + fruit_vegetables_nuts_points
    else:
        fruit_vegetables_nuts_points = 0
        positive_points = fiber_points + protein_points

    # Total score
    if fruit_vegetables_nuts_points < 5:
        score = negative_points - positive_points
    else:
        score = negative_points - fiber_points - protein_points

    # Nutri-Score
    if score <= -1:
        nutriscore = 'A'
    elif score <= 2:
        nutriscore = 'B'
    elif score <= 10:
        nutriscore = 'C'
    elif score <= 18:
        nutriscore = 'D'
    else:
        nutriscore = 'E'

    return nutriscore

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
