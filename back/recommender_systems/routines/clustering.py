### Ce fichier contient les scripts qui permettront de créer des catégories de repas ###
from app.models.cafe_model import MenuItem, Cafe
from app.services.cafe_service import CafeService
from app.schemas.cafe_schema import MenuItemUpdate
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils

import asyncio

from typing import List, Dict

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

def _numeric_foods(items: List[MenuItem]) -> List[List[float]]:
    data: list[list[float]] = []
    for item in items:
        infos: list[float] = list(item.nutritional_informations.values())
        data.append(infos)
    return data

# Create clusters based on the labels got from kmeans.
# It assumes that the items in the 'items' and 'data' lists in the method 'clustering'
#   have the same indexing: items[i] equiv data[i].
def _create_clusters(labels: np.array, items: List[MenuItem]) -> Dict[str, List[MenuItem]]:
    clusters: dict[str, list[MenuItem]] = {}
    for label, item in zip(labels, items):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(item)
    return clusters

# Create clusters using k-means algorithm.
# Create clusters from all the foods available in all cafe.
async def _clusters() -> Dict[str, List[MenuItem]]:
    items: list[MenuItem] = await DButils.get_all_items()
    data: list[list[float]] = _numeric_foods(items)
    n: int = len(data)

    # Normaize the data
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(data)

    # Find the best number of clusters using silhouette score.
    scores: list[float] = []
    for i in range(2, n+1):
        kmeans: KMeans = KMeans(n_clusters=i, random_state=42)
        scores.append(silhouette_score(normalized_data, kmeans.fit_predict(normalized_data)))
    max_score: float = max(scores)
    indexes: list[int] = Utilitaries.find_indices(scores, max_score)
    if len(indexes) > 1:
        k: int = scores[max(indexes)] + 1
    else: 
        k: int = scores.index(max_score) + 1
    
    # Apply k-means
    kmeans: KMeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(normalized_data)
    clusters = _create_clusters(kmeans.labels_, items)
    return clusters

# Update item's cluster in the database.
def update_item_cluster():
    all_cafe: list[Cafe] = asyncio.run( DButils.get_all_cafe() )
    clusters: dict[str, list[MenuItem]] = asyncio.run( _clusters() )
    for cluster in clusters.keys():
        for item in clusters[cluster]:
            cafes: List[Cafe] = Utilitaries.find_cafe_by_item(all_cafe, item)
            for cafe in cafes:
                item_data = {
                    "cluster": cluster
                }
                asyncio.run( CafeService.update_menu_item(cafe.slug, item.slug, MenuItemUpdate(**item_data)) )