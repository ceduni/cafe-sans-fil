from typing import List, Any, Tuple
from app.models.cafe_model import MenuItem, Cafe
from app.models.user_model import User
from app.models.order_model import Order, OrderedItem
from app.services.cafe_service import CafeService
from app.services.order_service import OrderService
from app.services.user_service import UserService
from collections import Counter
import uuid

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

# Get all users
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