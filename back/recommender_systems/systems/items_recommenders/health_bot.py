from typing import List, Dict
from app.models.cafe_model import MenuItem, Cafe
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
from tqdm import tqdm

# Sort items in descending order by health scores.
def sort_by_health_score(items: List[MenuItem]) -> List[str]:
    items_tuples: list[tuple[float, MenuItem]] = []

    for item in items:
        if 'health_score' not in item:
            item['health_score'] = Utilitaries.health_score(item)
        items_tuples.append( (item['health_score'], item['slug']) )

    sorted_items_tuples: list[tuple[float, MenuItem]] = sorted(items_tuples, reverse=False)

    sorted_items: List[str] = []
    
    for item_tuple in sorted_items_tuples:
        sorted_items.append(item_tuple[1])

    return sorted_items

# This method takes all the foods and return the foods with the highest 
# health score.
def main(all_cafe: List[Cafe]) -> Dict[str, List[str]]:
    recommendations: dict[str, List[str]] = {}
    for _, cafe in enumerate(tqdm(all_cafe, desc="Running health bot")):
        recommendations[cafe['slug']] = sort_by_health_score( DButils.get_cafe_items(cafe['slug']) )
    return recommendations


