### Algorithme 4.3 ###
from back.app.models.cafe_model import MenuItem, Cafe
from back.app.models.user_model import User

import numpy as np

# This algorithm recommand foods based on the specifications (preferences)
# and the allergens of the user.
def main(actual_cafe: Cafe, user: User) -> list[MenuItem]:
    user_allergens: list[dict] = user.allergens
    menu_items: list[MenuItem] = Cafe.menu_items
    allergenic_foods_list: list[MenuItem] = allergenic_foods(user_allergens, menu_items)
    user_preferences: list[str] = user.preferences
    clusters: dict = clusters_user_preference(actual_cafe)
    try:
        diet: dict = clusters[user_preferences[0]]
        recommendations: list[MenuItem] = diet[user_preferences[1]]
        return list(filter(lambda x: x not in allergenic_foods_list ,recommendations))
    except KeyError: # There is no foods satisfying the user specifications
        return []

# This method takes the list of the user allergens and return the foods
#  containing at least one of those allergens.
def allergenic_foods(user_allergens: list[dict], menu: list[MenuItem]) -> list[MenuItem]:
    allergenic_items: list[MenuItem] = []
    np_user_allergens: np.array[str] = np.array(user_allergens['names'])
    for item in menu:
        if len(item.allergens) > 0:
            item_allergens: np.array[str] = np.array(item.allergens)
            if len(np.intersect1d(np_user_allergens, item_allergens)) != 0:
                allergenic_items.append(item)
    return allergenic_items


# This method creates clusters based on the user preferences.
# It takes the actual cafe as parameter and returns a dictionnary
#
#{
# "diet": {
#       "category":{
#           [items]
#       }
#   }
#}

def clusters_user_preference(actual_cafe: Cafe) -> dict:
    items: list[MenuItem] = actual_cafe.menu_items
    clusters: dict = {}
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
        categories: dict = {}
        for item in items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)
        clusters[diet] = categories
    
    return clusters