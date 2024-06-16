### Algorithme 4.3 ###
from back.app.models.cafe_model import MenuItem, Cafe
from back.app.models.user_model import User

# This algorithm recommand foods based on the specifications (preferences)
# and the allergens of the user.
def main(actual_cafe: Cafe, user: User) -> list[MenuItem]:
    user_allergens: list[str] = user.allergens
    allergenic_foods_list: list[MenuItem] = allergenic_foods(user_allergens)
    user_preferences: list[str] = user.preferences
    clusters: dict = clusters_user_preference(actual_cafe)
    diet: dict = clusters[user_preferences[0]]
    recommendations: list[MenuItem] = diet[user_preferences[1]]
    return list(filter(lambda x: x not in allergenic_foods_list ,recommendations))

# This method takes the list of the user allergens and return the foods
#  containing at least one of those allergens.
def allergenic_foods(user_allergens: list[str]) -> list[MenuItem]:
    #TODO
    return

# This method creates clusters based on the user preferences.
def clusters_user_preference(actual_cafe: Cafe) -> dict:
    items: list[MenuItem] = actual_cafe.menu_items

    clusters = {}
    for item in items:
        if item.diet not in clusters:
            clusters[item.diet] = []
        clusters[item.diet].append(item)

    diets = list(clusters.keys())
    for diet in diets:
        items = clusters[diet]
        categories = {}
        for item in items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)
        clusters[diet] = categories
    
    return clusters