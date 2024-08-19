from app.models.cafe_model import MenuItem, Cafe
from app.models.user_model import User, DietProfile
from recommender_systems.utils import db_utils as DButils, utilitaries as Utils
import math
from typing import List, Dict, Any, Tuple

# This method regroups the list of items based on their diets.
def regroup_by_diet(items: List[MenuItem], user_diets: List[Dict[str, Any]]) -> Dict[str, List[Tuple[MenuItem, int]]]:
    try:
        if not isinstance(items, list):
            raise TypeError("Argument must be a list.")
        
        if len(items) == 0 or len(user_diets) == 0:
            return {}
        
        groups: Dict[str, List[Tuple[str, int]]] = {}
        for item in items:
            item_diets: List[str] = Utils.find_item_diets_for_user(item, user_diets)  # List of user's diets where the item can be eaten
            for diet in item_diets:
                if diet not in groups:
                    groups[diet] = []
                groups[diet].append((item, 1))  # Assign a basic score of 1 for matching diet

        return groups
    except TypeError as e:
        print(e)
        return {}

# Return a list containing only items that contain at most level 1 allergens, with their scores.
def remove_allergenic_items(items: List[MenuItem], user_allergens: Dict[str, int]) -> List[Tuple[str, int]]:
    result: List[Tuple[str, int]] = []
    if len(user_allergens) == 0 and len(items) != 0:
        return [(item['slug'], 1) for item in items]
    
    if len(items) == 0:
        return []
    
    allergens: set[str] = set()

    for allergen, level in user_allergens.items():
        if level >= 2:
            allergens.add(allergen)

    for item in items:
        if not set(item['ingredients']) & allergens:
            result.append((item['slug'], 1))  # Assign a basic score of 1 for being allergen-safe

    return result

def _get_valid_items(items: List[MenuItem], user_prefered_nutrients: Dict[str, int]) -> List[Tuple[str, int]]:
    valid_items: List[Tuple[str, int]] = []

    for nutrient, level in user_prefered_nutrients.items():
        nutrient_dv: float = Utils.get_nutrient_daily_value(nutrient.lower())

        low_bound: float = 0
        high_bound: float = 0

        if level == 1:
            low_bound, high_bound = 0, 90
        elif level == 2:
            low_bound, high_bound = 90, 110
        elif level == 3:
            low_bound, high_bound = 110, math.inf
        else:
            raise ValueError("Level must be between 1 and 3")
        for item in items:
            percentage_dv = (float(item['nutritional_informations'][nutrient.lower()]) / nutrient_dv) * 100
            if low_bound <= percentage_dv < high_bound:
                valid_items.append((item, 1))

    # Filter to keep only items that match all nutrient preferences
    valid_items = [(item, score) for item, score in valid_items]

    return valid_items

def _validate_inputs(actual_cafe: Dict[str, Any], user: Dict[str, Any]) -> None:
    """Validates the inputs for the main function."""
    if not isinstance(actual_cafe, dict):
        raise TypeError("Argument 1 must be a Dict")
    
    if not isinstance(user, dict):
        raise TypeError("Argument 2 must be a Dict")

    if 'slug' not in actual_cafe:
        raise KeyError("Argument actual_cafe must have a 'slug' attribute")
    
    if 'diet_profile' not in user:
        raise KeyError("Argument user must have a 'diet_profile' attribute")
    
def format_output(items: List[Tuple[str, int]]) -> Dict[str, int]:
    result: dict[str, int] = {}
    for item, score in items:
        if item not in result:
            result[item] = score
        result[item] += score
    return result

# This algorithm recommends foods based on the specifications (preferences)
# and the allergens of the user.
def main(actual_cafe: Cafe, user: User) -> Dict[str, int]:

    _validate_inputs(actual_cafe, user)
    
    menu_items: List[MenuItem] = DButils.get_cafe_items(actual_cafe['slug'])
    user_diets: List[Dict[str, Any]] = user['diet_profile']['diets']
    user_prefered_nutrients: Dict[str, int] = user['diet_profile']['prefered_nutrients']

    # No diets and no nutrients specified
    if not user_diets and not user_prefered_nutrients:
        recs: List[Tuple[str, int]] = remove_allergenic_items(menu_items, user['diet_profile']['allergens'])
        result = format_output(recs)
        return result if len(result) <= len(menu_items) else {}
    
    # Only nutrients specified
    if not user_diets and user_prefered_nutrients:  # Only nutrients specified
        try:
            valid_items: List[Tuple[MenuItem, int]] = _get_valid_items(menu_items, user_prefered_nutrients)
        except ValueError as e:
            print(e)
            return {}
        valid_items_2 = remove_allergenic_items([item for item, _ in valid_items], user['diet_profile']['allergens'])

        return format_output(valid_items_2)

    # Only diets specified
    if user_diets and not user_prefered_nutrients:  # Only diet specified
        items_clustered: Dict[str, List[Tuple[MenuItem, int]]] = regroup_by_diet(menu_items, user_diets)
        all_clusterd_items: List[Tuple[MenuItem, int]] = []
        
        for cluster in items_clustered.values():
            all_clusterd_items.extend(cluster)
        valid_items_2 = remove_allergenic_items([item for item, _ in all_clusterd_items], user['diet_profile']['allergens'])
        return format_output(valid_items_2)

    # Both nutrients and diets specified
    items_clustered: Dict[str, List[Tuple[MenuItem, int]]] = regroup_by_diet(menu_items, user_diets)
    all_clusterd_items: List[Tuple[MenuItem, int]] = []
    
    for cluster in items_clustered.values():
        all_clusterd_items.extend(cluster)

    try:
        valid_items: List[Tuple[MenuItem, int]] = _get_valid_items([item for item, _ in all_clusterd_items], user_prefered_nutrients)
    except ValueError as e:
        print(e)
        return []
    
    return format_output( remove_allergenic_items([item for item, _ in valid_items], user['diet_profile']['allergens']) )
