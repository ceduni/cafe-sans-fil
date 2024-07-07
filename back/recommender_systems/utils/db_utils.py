from typing import List
from app.models.cafe_model import MenuItem, Cafe
from app.models.user_model import User
from app.models.order_model import Order
from recommender_systems.utils.api_calls import *

#------------------------
#       Users
#------------------------

# Return the slug of all cafe where the user bought at least one item.
def get_user_visited_cafe(user: User) -> List[str]:
    params = {
        "page": 1,
        "limit": 40,
        "sort_by": "name"
    }
    auth_token = AuthApi.auth_login()
    user_orders, _ = OrderApi.get_user_orders(auth_token=auth_token, username=user['username'], params=params)
    visited_cafe: List[str] = []
    for order in user_orders:
        visited_cafe.append(order['cafe_slug']) if order['cafe_slug'] not in visited_cafe else None
    return visited_cafe

# Return the slugs of the items liked by the user.
def get_all_user_likes(user_id: str) -> List[str]:
    all_items: List[MenuItem] = get_all_items()
    items: List[str] = []
    for item in all_items:
        if user_id in item['likes']:
            items.append(item['slug'])
    return items

def get_user_likes_in_cafe(user_id: str, cafe_items: List[MenuItem]) -> List[str]:
    items = []
    for item in cafe_items:
        if user_id in item['likes']:
            items.append(item['slug'])
    return items

# Get all users.
def get_all_users() -> List[User]:
    query_params = {
        "page": 1,
        "limit": 20,
        "sort_by": "last_name"
    }
    auth_token = AuthApi.auth_login()
    users, _ = UserApi.get_users(auth_token=auth_token, params=query_params)
    return users

#------------------------
#       Orders
#------------------------

# Return the ids of all the user orders.
def get_user_orders(user: User) -> List[str]:
    params = {
        "page": 1,
        "limit": 40,
        "sort_by": "name"
    }
    auth_token = AuthApi.auth_login()
    orders, _ = OrderApi.get_user_orders(auth_token=auth_token, username=user['username'], params=params)
    return list(map(lambda x: x['order_id'], orders))

def get_all_orders(auth_token) -> List[str]:
    params = {
        "page": 1,
        "limit": 40,
        "sort_by": "name"
    }
    orders, _ = OrderApi.get_orders(auth_token=auth_token, params=params)
    return orders

def get_order_items(order_id: str) -> List[str]:
    params = {
        "page": 1,
        "limit": 40,
        "sort_by": "name"
    }
    order = OrderApi.get_order(order_id, params)
    items = list(map(lambda x: x['slug'], order['items']))
    return items

def get_order(order_id: str) -> Order:
    params = {
        "page": 1,
        "limit": 40,
        "sort_by": "name"
    }
    order = OrderApi.get_order(order_id, params)
    return order

#-----------------------------
#       Cafe and Items
#-----------------------------

#Description: Get all items from a cafe.
def get_cafe_items(cafe_slug: str) -> List[MenuItem]:
    query_params = {
        "page": 1,
        "limit": 40
    }
    response, _ = CafeApi.get_all_items(cafe_slug, query_params)
    return response

def get_item(cafe_slug: str, item_slug: str) -> MenuItem:
    auth_token = AuthApi.auth_login()
    response, _ = CafeApi.get_item(auth_token=auth_token, cafe_slug=cafe_slug, item_slug=item_slug)
    return response

# Get all items.
def get_all_items() -> List[MenuItem]:
    query_params = {
        "page": 1,
        "limit": 40
    }
    all_cafes: list[Cafe] = get_all_cafe()
    all_items: List[MenuItem] = []
    for cafe in all_cafes:
        cafe_slug = cafe['slug']
        response, _ = CafeApi.get_all_items(cafe_slug, query_params)
        all_items.extend(response)
    return all_items

# Get all cafe.
def get_all_cafe() -> List[Cafe]:
    query_params = {
        "page": 1,
        "limit": 40,
        "sort_by": "name"
    }
    auth_token = AuthApi.auth_login()
    cafes, _ = CafeApi.get_cafes(auth_token=auth_token, params=query_params)
    return cafes
