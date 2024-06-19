### Algorithme 4.3 ###
from back.app.models.cafe_model import MenuItem, Cafe
from back.app.models.user_model import User, DietProfile
from typing import List, Dict
import utilitaries as Utilitaries
import numpy as np

# This method creates clusters based on the user preferences.
# It takes the actual cafe as parameter and returns a dictionnary
#
#{
# "diet": {
#       "category_name": [items],
#   },
#}
def diet_category_cluster(items: List[MenuItem]) -> Dict[str, Dict[str, List[MenuItem]]]:
    clusters: dict[str, dict[str, list[MenuItem]]] = {}
    for item in items:
        diets: list[str] = item.diets
        if len(diets) > 0:
            for diet in diets:
                if diet not in clusters:
                    if diet == "":
                        clusters["no_diet"] = []
                        clusters["no_diet"].append(item)
                    else:
                        clusters[diet] = []
                        clusters[diet].append(item)
                else:
                    clusters[diet].append(item)

    diets: list[str] = list(clusters.keys())
    for diet in diets:
        items: list[MenuItem] = clusters[diet]
        categories: dict[str, list[MenuItem]] = {}
        for item in items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)
        clusters[diet] = categories
    
    return clusters

# This method takes the list of the user allergens and return the foods
#  containing at least one of those allergens.
def allergenic_foods(user_allergens: Dict[str, int], menu: List[MenuItem]) -> List[MenuItem]:
    allergenic_items: list[MenuItem] = []
    np_user_allergens: np.array[str] = np.array( list(user_allergens.keys()) )
    for item in menu:
        if len(item.allergens) > 0:
            item_allergens: np.array[str] = np.array(item.allergens)
            if len(np.intersect1d(np_user_allergens, item_allergens)) != 0:
                allergenic_items.append(item)
    return allergenic_items

# This algorithm recommand foods based on the specifications (preferences)
# and the allergens of the user.
def main(actual_cafe: Cafe, user: User) -> List[str]:
    diet_profile: DietProfile = user.diet_profile
    user_allergens: dict[str, int] = diet_profile.allergens
    menu_items: list[MenuItem] = actual_cafe.menu_items
    allergenic_foods_list: list[MenuItem] = allergenic_foods(user_allergens, menu_items)
    user_preferences: list[list[str]] = [diet_profile.diets, diet_profile.food_categories]
    clusters: dict[str, dict[str, list[MenuItem]]] = diet_category_cluster(menu_items)
    try:
        prefered_diets: list[str] = user_preferences[0]
        prefered_categories: list[str] = user_preferences[1]
        categories: list[dict[str, list[MenuItem]]] = list(map(lambda x: clusters[x], prefered_diets))
        recommendations: list[MenuItem] = []
        for prefered_category in prefered_categories:
            for category in categories:
                if prefered_category in category:
                    recommendations.extend(category[prefered_category])
        valid_recommendations: list[MenuItem] = list( filter(lambda x: x if x not in allergenic_foods_list else None ,recommendations) )
        return Utilitaries.items_ids(valid_recommendations)
    except KeyError: # There is no foods satisfying the user specifications
        return []