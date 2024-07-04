# Ce fichier contient le code des algorithmes de la section 2 du document
#   "Logique" du wiki.
from typing import List, Any, Tuple
from app.models.cafe_model import MenuItem, Cafe
from recommender_systems.utils import db_utils as DButils
from app.models.user_model import User
from app.models.order_model import Order, OrderedItem
from recommender_systems.utils.api_calls import *
from typing import List, Dict, Set
import uuid

#------------------------
#       Users
#------------------------

# Calculate the similarity between two users using jaccard similarity.
def users_similarity(u_list: List[List[str] | Set[str]], v_list: List[List[str] | Set[str]]) -> float:
    J: list[float] = []
    for i in range(0, len(v_list)):
        resized_array: tuple[list[str]] = reshape( list(u_list[i]), list(v_list[i]) )
        j: float = jaccard_similarity( set(resized_array[0]), set(resized_array[1]) )
        J.append(j)
    score: float = sum(J)
    return score

def jaccard_similarity(set1: Set, set2: Set) -> float:
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

#-----------------------
#       Items
#-----------------------

# This method take a dictionnary : { item slug: number of purchases }.
# It returns a list of item slug sorted in descending
#   order (most item bought to least item bought).
def _sort_items_by_occurences(map: Dict[str, int]) -> List[str]:
    tuple_items: list[tuple[int, str]] = []
    for key in map.keys():
        tuple_items.append((map[key], key))
    sorted_items: list[tuple[int, str]] = sorted(tuple_items, reverse=True)
    return [ item[1] for item in sorted_items ]

# Take a list of orders and return a list of item slug sorted in descending
#   order (most item bought to least item bought).
def most_bought_items(all_orders: List[Order]) -> List[str]:
    items_map: dict[str, int] = {}
    for order in all_orders:
        items: List[OrderedItem] = order['items']
        for item in items:
            if item['item_slug'] not in items_map:
                items_map[item['item_slug']] = 1
            else:
                items_map[item['item_slug']] += 1
    return _sort_items_by_occurences(items_map)

# This method takes a list of items and sort those items in descending order
#   (most liked item to least like item).
# It returns k items. 
# IF k < 0, then no size is specified so it returns all the items
#   sorted.
def most_liked_items(items: List[MenuItem], k: int = -1) -> List[str]:
    if k < 0:
        k = len(items)

    likes: list[int] = []
    for item in items:
        likes.append(len(item['likes']))
    
    most_liked_items: list[str] = []
    for _ in range(k):
        max_likes = max(likes)
        index = likes.index(max_likes)
        most_liked_items.append(items[index]['slug'])
        likes[index] = -1

    return most_liked_items

# Takes a list of items as parameter and returns a list that contains the slugs
#   of the items.
def items_slugs(items: List[MenuItem]) -> List[str]:
    return list(map(lambda x: x['slug'], items))

# This method takes a list of orders ids and return a list of all the items
#   (slugs of the items) contained in these orders.
def list_items(orders_ids: List[str]) -> List[str]:
    all_slugs: list[str] = []
    for id in orders_ids:
        order, _ = OrderApi.get_order(id)
        print(order)
        ordered_items: list[OrderedItem] = order['items']     
        slugs: list[str] = []       
        for item in ordered_items:
            slugs.append(item['slug'])
        all_slugs.extend(slugs)
    return all_slugs

def regroup_by_cluster(items: List[MenuItem]) -> Dict[str, List[str]]:
    groups: dict[str, list[str]] = {}
    for item in items:
        if item['cluster'] not in groups:
            groups[item['cluster']] = []
        groups[item['cluster']].append(item['slug'])
    return groups
    
# Takes a list of item slugs and a cafe slug and returns a list of slugs of
#   items sold in this cafe.
def filter_items_by_cafe(slugs: List[str], cafe_slug: str) -> List[str]:
    items: list[str] = []
    for slug in slugs:
        retrived_item: MenuItem = CafeApi.get_item(cafe_slug, slug)
        if retrived_item != None:
            items.append(retrived_item['slug']) if retrived_item['slug'] not in items else None
    return items

# This method takes a user and a cafe as parameters and return
#   a list of items not yet bought by the user in this cafe.
def meal_not_consumed(cafe: Cafe, user: User) -> List[str]:
    cafe_slug = cafe['slug']
    order_history: list[str] = DButils.get_user_orders(user)
    oredered_items_slugs: list[str] = []
    for order_id in order_history:
        oredered_items_slugs.extend(DButils.get_order_items(order_id))
    
    meal_not_consumed: list[str] = []
    for item_slug in oredered_items_slugs:
        item = DButils.get_item(cafe_slug, item_slug)
        if item != None:
            meal_not_consumed.append(item['slug'])

    return meal_not_consumed

#-----------------------
#       Cafe
#-----------------------

# Take a list of cafe and an item and return the list of cafe selling the item.
def find_cafe_by_item(cafe_list: List[Cafe], item: MenuItem) -> List[Cafe]:
    cafes = []
    for cafe in cafe_list:
        items = DButils.get_cafe_items(cafe['slug'])
        if item in items:
            cafes.append(cafe)
    return cafes

#-----------------------
#       Others
#-----------------------

# Find the indexes of an element in an array
def find_indexes(input_list, value) -> List[int]:
    return [i for i, x in enumerate(input_list) if x == value]

# Calculate the nutriscore of an item
def health_score(item: MenuItem) -> float:
    nutri_info: dict[str, float] = item['nutritional_informations']

    negative_points_max = 10
    positive_points_max = 5

    # Negative points
    energy_points = min(max(int( float(nutri_info["calories"]) / 335), 0), negative_points_max)
    sugar_points = min(max(int( float(nutri_info["sugar"]) / 4.5), 0), negative_points_max)
    saturated_fat_points = min(max(int( float(nutri_info["saturated_fat"]) / 1), 0), negative_points_max)
    sodium_points = min(max(int( float(nutri_info["sodium"]) / 90), 0), negative_points_max)
    negative_points = energy_points + sugar_points + saturated_fat_points + sodium_points

    # Positive points
    fiber_points = min(max(int( float(nutri_info["fiber"]) / 0.9), 0), positive_points_max)
    protein_points = min(max(int( float(nutri_info["protein"]) / 1.6), 0), positive_points_max)
    if nutri_info["percentage_fruit_vegetables_nuts"]:
        fruit_vegetables_nuts_points = min(max(int( float(nutri_info["percentage_fruit_vegetables_nuts"]) / 40), 0), positive_points_max)
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
    #if score <= -1:
    #    nutriscore = 'A'
    #elif score <= 2:
    #    nutriscore = 'B'
    #elif score <= 10:
    #    nutriscore = 'C'
    #elif score <= 18:
    #    nutriscore = 'D'
    #else:
    #   nutriscore = 'E'

    return score

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
