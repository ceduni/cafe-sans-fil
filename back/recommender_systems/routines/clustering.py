### Ce fichier contient les scripts qui permettront de créer des catégories de repas ###
from app.models.cafe_model import MenuItem, Cafe
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
from recommender_systems.utils.api_calls import CafeApi, AuthApi

from typing import List, Dict

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from app.models.cafe_model import NutritionInfo

from tqdm import tqdm

# Take a list of items and return a list of lists of numeric values
#   representing the nutritional informations of each item.
def numeric_foods(items: List[MenuItem]) -> List[List[float]]:
    data: list[list[float]] = []
    for item in items:
        item_infos: NutritionInfo = item['nutritional_informations']
        infos: list[float] = [
            float(item_infos['calories']) if item_infos['calories'] else 0, 
            float(item_infos['lipid']) if item_infos['lipid'] else 0,
            float(item_infos['protein']) if item_infos['protein'] else 0,
            float(item_infos['carbohydrates']) if item_infos['carbohydrates'] else 0,
            float(item_infos['sugar']) if item_infos['sugar'] else 0,
            float(item_infos['sodium']) if item_infos['sodium'] else 0,
            float(item_infos['fiber']) if item_infos['fiber'] else 0,
            float(item_infos['vitamins']) if item_infos['vitamins'] else 0,
            float(item_infos['saturated_fat']) if item_infos['saturated_fat'] else 0,
            float(item_infos['percentage_fruit_vegetables_nuts']) if item_infos['percentage_fruit_vegetables_nuts'] else 0,
        ]
        data.append(infos)
    return data

# Create clusters based on the labels got from kmeans.
# It assumes that the items in the 'items' and 'data' lists in the method 'clustering'
#   have the same indexing: items[i] equiv data[i].
def create_clusters(labels: np.array, items: List[MenuItem]) -> Dict[str, List[MenuItem]]:
    clusters: dict[str, list[MenuItem]] = {}

    if len(items) == 0:
        raise ValueError("Items list cannot be empty")

    if len(labels) == 0:
        clusters['0'] = []
        for item in items:
            clusters['0'].append(item)
        return clusters

    for label, item in zip(labels, items):
        if str(label) not in clusters:
            clusters[str(label)] = []
        clusters[str(label)].append(item)
    return clusters

# Create clusters using k-means algorithm.
# Create clusters from all the foods available in all cafe.
def _clusters() -> Dict[str, List[MenuItem]]:
    items: list[MenuItem] = DButils.get_all_items()
    data: list[list[float]] = numeric_foods(items)
    n: int = len(data)

    # Normaize the data
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(data)

    # Find the best number of clusters using silhouette score.
    scores: list[float] = []
    for _, i in enumerate( tqdm(range(2, n-1), desc="Creating clusters") ):
        kmeans: KMeans = KMeans(n_clusters=i, random_state=42)
        scores.append(silhouette_score(normalized_data, kmeans.fit_predict(normalized_data)))
    max_score: float = max(scores)
    indexes: list[int] = Utilitaries.find_indexes(scores, max_score)
    if len(indexes) > 1:
        k: int = scores[max(indexes)] + 1
    else: 
        k: int = scores.index(max_score) + 1
    
    # Apply k-means
    kmeans: KMeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(normalized_data)
    try:
        clusters = create_clusters(kmeans.labels_, items)
    except ValueError as e:
        print(e)
        clusters = {}

    return clusters

# Update item's cluster in the database.
def update_item_cluster():
    auth_token = AuthApi.auth_login()
    all_cafe: list[Cafe] = DButils.get_all_cafe()
    clusters: dict[str, list[MenuItem]] = _clusters()
    for _, cluster in enumerate(tqdm(clusters.keys(), desc="Updating item's cluster")):
        for item in clusters[cluster]:
            cafes: List[Cafe] = Utilitaries.find_cafe_by_item(all_cafe, item)
            for cafe in cafes:
                item_data = {
                    "cluster": cluster
                }
                CafeApi.update_item(auth_token=auth_token, cafe_slug=cafe['slug'], item_slug=item['slug'], json_data=item_data) 
