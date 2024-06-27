from typing import List, Dict
from app.models.cafe_model import MenuItem, Cafe
from recommender_systems.utils import utilitaries as Utilitaries

# This method takes all the foods and return the foods with the highest 
# health score.
def main(all_cafe: List[Cafe]) -> Dict[str, List[str]]:
    recommendations: dict[str, List[str]] = {}
    for cafe in all_cafe:
        recommendations[cafe.slug] = sort_by_health_score(cafe.menu_items)
    return recommendations


# Sort items in descending order by health scores.
def sort_by_health_score(items: List[MenuItem]) -> List[str]:
    items_tuples: list[tuple[float, MenuItem]] = []

    for item in items:
        items_tuples.append( (item.health_score, item) )

    sorted_items_tuples: list[tuple[float, MenuItem]] = sorted(items_tuples, reverse=False)

    sorted_items: List[MenuItem] = []
    
    for item_tuple in sorted_items_tuples:
        sorted_items.append(item_tuple[1])

    return Utilitaries.items_slugs(sorted_items)