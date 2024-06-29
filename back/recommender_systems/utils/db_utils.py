from typing import List, Any, Tuple
from app.models.cafe_model import MenuItem, Cafe
from app.models.user_model import User
from app.models.order_model import Order, OrderedItem
from app.services.cafe_service import CafeService
from app.services.order_service import OrderService
from app.services.user_service import UserService
from collections import Counter
import uuid

# Return the slug of all cafe where the user bought at least one item.
async def get_user_visited_cafe(user: User) -> List[str]:
    user_orders: List[Order] = await get_user_orders(user)
    visited_cafe: List[str] = []
    for order in user_orders:
        visited_cafe.append(order.cafe_slug) if order.cafe_slug not in visited_cafe else None
    return visited_cafe

# Return the ids of all the user orders.
async def get_user_orders(user: User) -> List[str]:
    filters = {
        "page": 1,
        "limit": 40,
        "sort_by": "name"
    }
    orders: List[Order] = await OrderService.list_orders_for_user(user.username, **filters)
    return list(map(lambda x: x.id, orders))

# Return the slugs of the items liked by the user.
async def get_user_likes(user: User) -> List[str]:
    all_items: List[MenuItem] = await get_all_items()
    items: List[str] = []
    for item in all_items:
        if user.id in item.likes:
            items.append(item.slug)
    return items

# Get all items.
async def get_all_items() -> List[MenuItem]:
    query_params = {
        "cafe_id_or_slug": None,
        "page": 1,
        "limit": 40,
        "sort_by": "nothing"
    }
    items: list[MenuItem] = await CafeService.list_menu_items(**query_params)
    return items

# Get all cafe.
async def get_all_cafe() -> List[Cafe]:
    query_params = {
        "page": 1,
        "limit": 40,
        "sort_by": "name"
    }
    cafes: list[Cafe] = await CafeService.list_cafes(**query_params)
    return cafes

# Get all users.
async def get_all_users() -> List[User]:
    filters = {
        "page": 1,
        "limit": 20,
        "sort_by": "last_name"
    }
    dict_users: list[dict[str, Any]] = await UserService.list_users(**filters)
    users: list[User] = []
    for u in dict_users:
        users.append(User(
            id= u['user_id'],
            email= u["email"],
            matricule= u["matricule"],
            username= u["username"],
            first_name= u["first_name"],
            last_name= u["last_name"],
            photo_url= u["photo_url"],
        ))
    return users
