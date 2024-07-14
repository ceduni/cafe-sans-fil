from typing import List, Dict
from app.models.cafe_model import MenuItem, Cafe
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
from tqdm import tqdm

# This method takes all the foods and return the foods with the highest 
# health score.
def main(all_cafe: List[Cafe]) -> Dict[str, List[str]]:
    recommendations: dict[str, List[str]] = {}
    for _, cafe in enumerate(tqdm(all_cafe, desc="Running health bot")):
        recommendations[cafe['slug']] = Utilitaries.sort_by_health_score( DButils.get_cafe_items(cafe['slug']) )
    return recommendations


