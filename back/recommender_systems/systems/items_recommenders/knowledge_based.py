### Algorithme 4.3 ###
from app.models.cafe_model import MenuItem, Cafe
from app.models.user_model import User, DietProfile
from recommender_systems.utils import db_utils as DButils
from typing import List, Dict

# This method creates clusters based on the user preferences.
# It takes the actual cafe as parameter and returns a dictionnary
#
#{
# "diet": {
#       "category_name": [items],
#   },
#}
def diet_category_cluster(items: List[MenuItem]) -> Dict[str, Dict[str, List[str]]]:
    try:
        if isinstance(items, list) == False or len(items) == 0:
            raise TypeError("Argument must be a list of MenuItem")

        clusters: dict[str, dict[str, list[str]]] = {}
        for item in items:
            diets: list[str] = item['diets']
            if len(diets) > 0:
                for diet in diets:
                    if diet not in clusters:
                        clusters[diet] = []
                        clusters[diet].append(item)
                    else:
                        clusters[diet].append(item)
            else:
                clusters["no_diet"] = []
                clusters["no_diet"].append(item)

        diets: list[str] = list(clusters.keys())
        for diet in diets:
            items: list[str] = clusters[diet]
            categories: dict[str, list[str]] = {}
            for item in items:
                if item['category'] not in categories:
                    categories[item['category']] = []
                categories[item['category']].append(item['slug'])
            clusters[diet] = categories
        
        return clusters
    except TypeError as e:
        print(e)
        return {}

# This method takes the list of the user allergens and return the items slugs
#  containing at least one of those allergens.
def allergenic_foods(user_allergens: Dict[str, int], menu: List[MenuItem]) -> List[str]:
    try:
        if isinstance(user_allergens, dict) == False:
            raise TypeError("Argument1 must be a dictionnary.")
        
        if isinstance(menu, list) == False:
            raise TypeError("Argument2 must be a list.")
        
        if user_allergens == {} or len(menu) == 0:
            return []
        allergenic_items: list[str] = []
        set_user_allergens: set = set( list(user_allergens.keys()) )
        for item in menu:
            if len(item['allergens']) > 0:
                item_allergens: set = set(item['allergens'])
                if len(set_user_allergens.intersection(item_allergens)) != 0:
                    allergenic_items.append(item['slug'])
        return allergenic_items

    except TypeError as e:
        print(e)
        return []

def filter_by_categories(categories: List[Dict[str, List[str]]], prefered_categories: List[str]) -> list[str]:
    recommendations: list[str] = []
    for category in categories:
        for prefered_category in prefered_categories:
            if prefered_category in category:
                recommendations.extend(category[prefered_category])
    return recommendations

#TODO: Implement filter by nutrients preferences
def filter_by_nutrients() -> list[str]:
    return []

# This algorithm recommand foods based on the specifications (preferences)
# and the allergens of the user.
def main(actual_cafe: Cafe, user: User) -> List[str]:
    try:
        if isinstance(actual_cafe, dict) == False:
            raise TypeError("Argument 1 must be a Dict.")
        
        if isinstance(user, dict) == False:
            raise TypeError("Argument 2 must be a Dict.")
        
        if len(actual_cafe) == 0 or len(user) == 0:
            return []

        diet_profile: DietProfile = user['diet_profile']
        user_allergens: dict[str, int] = diet_profile['allergens']
        menu_items: list[MenuItem] = DButils.get_cafe_items(actual_cafe['slug'])
        allergenic_foods_list: list[str] = allergenic_foods(user_allergens, menu_items)
        clusters: dict[str, dict[str, list[MenuItem]]] = diet_category_cluster(menu_items)
        try:
            prefered_diets: list[str] = diet_profile['diets']
            prefered_categories: list[str] = diet_profile['food_categories']

            if len(prefered_diets) > 0 and len(prefered_categories) == 0: # Diets prefered but no categories
                categories: list[dict[str, list[str]]] = []
                recommendations: list[str] = []
                for diet in prefered_diets:
                    categories.append(clusters[diet]) if diet in prefered_diets else None
                for category in categories:
                    for key in category.keys():
                        recommendations.extend(category[key])

            elif len(prefered_diets) == 0 and len(prefered_categories) > 0: # No diets prefered but categories prefered
                categories: list[dict[str, list[str]]] = list( clusters.values() )
                recommendations: list[str] = filter_by_categories(categories, prefered_categories)

            elif len(prefered_diets) > 0 and len(prefered_categories) > 0: # Diets and categories prefered
                categories: list[dict[str, list[str]]] = []

                for diet in prefered_diets:
                    if diet in prefered_diets:
                        categories.append(clusters[diet])

                recommendations: list[str] = filter_by_categories(categories, prefered_categories)
            
            else: # No specifications
                recommendations: list[str] = []
                for diet in clusters.keys():
                    categories: dict[str, list[str]] = clusters[diet]
                    for category in categories.keys():
                        recommendations.extend(categories[category])

            if len(allergenic_foods_list) > 0:
                valid_recommendations: list[str] = list( filter(lambda x: x if x not in allergenic_foods_list else None ,recommendations) )
            else:
                valid_recommendations = recommendations
            return list( set(valid_recommendations) )
        except KeyError: # There is no foods satisfying the user specifications
            return []
    except TypeError as e:
        print(e)
        return []