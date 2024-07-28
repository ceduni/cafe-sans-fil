### Algorithme 4.3 ###
from app.models.cafe_model import MenuItem, Cafe
from app.models.user_model import User, DietProfile
from recommender_systems.utils import db_utils as DButils, utilitaries as Utils
import math
from typing import List, Dict, Any

# This method regroups the list of items based on there diets.
def regroup_by_diet(items: List[MenuItem], user_diets: List[Dict[str, str | list[MenuItem]]]) -> Dict[str, List[MenuItem]]:
    try:
        if isinstance(items, list) == False:
            raise TypeError("Argument must be a list.")
        
        if len(items) == 0 or len(user_diets) == 0:
            return {}
        
        groups: dict[str, list[str]] = {}
        for item in items:
            item_diets: list[str] = Utils.find_item_diets_for_user(item, user_diets) # List of uer's diets where the item can be eaten
            for diet in item_diets:
                if diet not in groups:
                    groups[diet] = []
                groups[diet].append(item)

        return groups
    except TypeError as e:
        print(e)
        return {}

# Return a list containing only items that contains at most level 1 allergens.
def remove_allergenic_items(items: List[MenuItem], user_allergens: Dict[str, int]) -> List[str]:
    result: set[str] = set()
    if len(user_allergens) == 0 and len(items) != 0:
        return list( map(lambda x: x['slug'], items) )
    
    if len(items) == 0:
        return []
    
    allergens: set[str] = set()

    for allergen, level in zip(user_allergens.keys(), user_allergens.values()):
        if level >= 2:
            allergens.add(allergen)

    for item in items:
        if len( set(item['ingredients']) & allergens ) == 0:
            result.add(item['slug'])

    return list(result)

def _get_valid_items(items: List[MenuItem], user_prefered_nutrients: dict[str, int]) -> list[MenuItem]:
    valid_items: set[str] = set()

    for nutrient, level in zip(user_prefered_nutrients.keys(), user_prefered_nutrients.values()):
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

        valid_items_for_nutrient: list[str] = []
        for item in items:

            percentage_dv = ( float( item['nutritional_informations'][nutrient.lower()] ) / nutrient_dv ) * 100
            if low_bound <= percentage_dv < high_bound:
                valid_items_for_nutrient.append(item)

        valid_items_for_nutrient_set = set(map(lambda x: x['slug'] ,valid_items_for_nutrient))

        if len(valid_items) == 0:
            valid_items = valid_items_for_nutrient_set

        valid_items = valid_items.intersection(valid_items_for_nutrient_set)

    result: list[MenuItem] = []
    for item_slug in valid_items:
        result.extend( list( filter(lambda x: x['slug'] == item_slug, items) ) )

    return result

def _validate_inputs(actual_cafe: Dict[str, Any], user: Dict[str, Any]) -> None:
    """Validates the inputs for the main function."""
    if isinstance(actual_cafe, dict) == False:
        raise TypeError("Argument 1 must be a Dict")
    
    if isinstance(user, dict) == False:
        raise TypeError("Argument 2 must be a Dict")

    if 'slug' not in actual_cafe.keys():
        raise KeyError("Argument actual_cafe must have a 'slug' attribute")
    
    if 'diet_profile' not in user.keys():
        raise KeyError("Argument user must have a 'diet_profile' attribute")

#TODO: Update tests.
# This algorithm recommand foods based on the specifications (preferences)
# and the allergens of the user.
def main(actual_cafe: Cafe, user: User) -> List[str]:

    _validate_inputs(actual_cafe, user)
    
    menu_items: list[MenuItem] = DButils.get_cafe_items(actual_cafe['slug'])
    user_diets: list[dict[str, str | list[str]]] = user['diet_profile']['diets']
    user_prefered_nutrients: dict[str, int] = user['diet_profile']['prefered_nutrients']

    

    # No diets and no nutrients specified
    if not user_diets and not user_prefered_nutrients:
        recs: list[str] = remove_allergenic_items(menu_items, user['diet_profile']['allergens'])
        return recs if len(recs) <= len(menu_items) else []
    
    # Only nutrients specified
    if not user_diets and user_prefered_nutrients: # Only nutrients specified
        valid_items: list[MenuItem] = _get_valid_items(menu_items, user_prefered_nutrients)
        return remove_allergenic_items(valid_items, user['diet_profile']['allergens'])
    
    # Only diets specified
    if user_diets and not user_prefered_nutrients: # Only diet specified
        items_clustered: dict[str, list[MenuItem]] = regroup_by_diet(menu_items, user_diets)
        all_clusterd_items: list[MenuItem] = list(items_clustered.values())
        all_clusterd_items_merged: list[MenuItem] = []
        
        for cluster in all_clusterd_items:
            all_clusterd_items_merged.extend(cluster)

        return remove_allergenic_items(all_clusterd_items_merged, user['diet_profile']['allergens'])

    # Both nutrients and diets specified
    items_clustered: dict[str, list[MenuItem]] = regroup_by_diet(menu_items, user_diets)
    all_clusterd_items: list[MenuItem] = list(items_clustered.values())
    all_clusterd_items_merged: list[MenuItem] = []
    
    for cluster in all_clusterd_items:
        all_clusterd_items_merged.extend(cluster)

    valid_items: list[MenuItem] = _get_valid_items(all_clusterd_items_merged, user_prefered_nutrients)

    return remove_allergenic_items(valid_items, user['diet_profile']['allergens'])
