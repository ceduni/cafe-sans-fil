from collections import Counter
from typing import List, Dict, Tuple
from app.models.cafe_model import MenuItem, Cafe
from app.models.user_model import User, Diet
from app.services.cafe_service import CafeService
from app.services.user_service import UserService

def find_invalid_items_for_diet(items: List[MenuItem], diets: List[Diet]) -> List[Dict[str, str]]:
    invalid_items = []
    for diet in diets:
        forbidden_foods_set = set(diet.forbidden_foods)
        for item in items:
            if forbidden_foods_set.intersection(item.ingredients):
                invalid_items.append({"item_id": item.item_id, "name": item.name})
    return invalid_items

def get_users_and_cafes() -> Tuple[List[User], List[Cafe]]:
    user_query = {"sort_by": "last_name", "page": 1, "limit": 70}
    cafe_query = {"sort_by": "name", "page": 1, "limit": 20}
    
    users = UserService.list_users(user_query)
    cafes = CafeService.list_cafes(cafe_query)
    
    return users, cafes

def find_items_not_in_diets() -> List[Dict[str, str]]:
    users, cafes = get_users_and_cafes()

    all_invalid_items = []
    for user in users:
        user_invalid_items: list[dict[str, str]] = []
        for cafe in cafes:
            user_invalid_items.extend(find_invalid_items_for_diet(cafe.menu_items, user.diet_profile.diets))

        for item in user_invalid_items:
            if item not in all_invalid_items:
                all_invalid_items.append(item)

    # Remove duplicates and count occurrences
    item_counts = Counter(item['item_id'] for item in all_invalid_items)
    unique_items = {item['item_id']: item for item in all_invalid_items}.values()

    result = [
        {"name": item['name'], "item_id": item['item_id'], "count": item_counts[item['item_id']]}
        for item in unique_items
    ]

    return result