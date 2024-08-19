from collections import Counter
from typing import List, Dict, Tuple
from app.models.cafe_model import MenuItem, Cafe
from app.models.user_model import User, Diet
from app.services.cafe_service import CafeService
from app.services.user_service import UserService
import re

# def find_invalid_items_for_diet(items: List[MenuItem], diets: List[Diet]) -> List[Dict[str, str]]:
#     invalid_items = []
#     for diet in diets:
#         forbidden_foods_set = set(diet.forbidden_foods)
#         for item in items:
#             if forbidden_foods_set.intersection(item.ingredients):
#                 invalid_items.append({"item_id": item.item_id, "name": item.name})
#     return invalid_items

def find_missing_items(items: List[MenuItem], diets: List[Diet]) -> List[str]:
    missing_items = []
    formatted_items_name_set = set( [format_name(item.name) for item in items] )
    for diet in diets:
        desired_items_map = format_names_map(diet['desired_foods'])
        formatted_missing_items = list( set( desired_items_map.keys() ) - formatted_items_name_set )
        missing_items.extend([ desired_items_map[item] for item in formatted_missing_items ])
    
    return list( set( missing_items ) )

def format_names_map(names: List[str]) -> Dict[str, str]:
    regex_pattern = r'[\s+\\.,!;_\'"-]'
    names_map = {}
    for name in names:
        names_map[ re.sub(regex_pattern, '', name) ] = name
    return names_map

def format_name(name: str) -> str:
    name = name.lower()
    regex_pattern = r'[\s+\\.,!;_\'"-]'
    return re.sub(regex_pattern, '', name)

async def _get_users_and_cafes() -> Tuple[List[User], List[Cafe]]:
    user_query = {"sort_by": "last_name", "page": 1, "limit": 70}
    cafe_query = {"sort_by": "name", "page": 1, "limit": 20}
    
    users = await UserService.list_users(**user_query)
    cafes = await CafeService.list_cafes(**cafe_query)
    
    return users, cafes

async def main() -> List[Dict[str, str]]:
    users, cafes = await _get_users_and_cafes()

    all_invalid_items: List[str] = []
    for user in users:
        user_diets = user['diet_profile']['diets']
        checked_diets = [diet for diet in user_diets if diet['checked']]
        if checked_diets:
            for short_cafe in cafes:
                cafe = await CafeService.retrieve_cafe(short_cafe.slug)
                all_invalid_items.extend(find_missing_items(cafe.menu_items, checked_diets))

    # Remove duplicates and count occurrences
    item_counts = Counter(all_invalid_items)

    item_list = []
    added_items_names = []

    for item in all_invalid_items:
        if item not in added_items_names:
            item_list.append({"name": item, "count": item_counts[item]})
            added_items_names.append(item)

    return item_list