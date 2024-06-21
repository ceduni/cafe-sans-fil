from typing import List, Dict
from app.models.cafe_model import MenuItem, Cafe

# This method takes all the foods and return the foods with the highest 
# health score.
def main(all_cafe: List[Cafe]) -> Dict[str, List[MenuItem]]:
    recommendations: dict[str, List[MenuItem]] = {}
    for cafe in all_cafe:
        recommendations[cafe.slug] = sort_by_health_score(cafe.menu_items)
    return recommendations


# Sort items in descending order by health scores.
def sort_by_health_score(items: List[MenuItem]) -> List[MenuItem]:
    items_tuples: list[tuple[float, MenuItem]] = []

    for item in items:
        items_tuples.append( (item.health_score, item) )

    sorted_items_tuples: list[tuple[float, MenuItem]] = sorted(items_tuples, reverse=True)

    sorted_items: List[MenuItem] = []
    
    for item_tuple in sorted_items_tuples:
        sorted_items.append(item_tuple[1])

    return sorted_items
