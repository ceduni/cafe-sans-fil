### Ce fichier contient les scripts qui permettront de créer des catégories de repas ###
from app.models.cafe_model import MenuItem
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils

import asyncio

from typing import List, Dict

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

def numeric_foods(items: List[MenuItem]) -> List[List[float]]:
    data: list[list[float]] = []
    for item in items:
        infos: list[float] = list(item.nutritional_informations.values())
        data.append(infos)
    return data

# Create clusters based on the labels got from kmeans.
# It assumes that the items in the 'items' and 'data' lists in the method 'clustering'
#   have the same indexing: items[i] equiv data[i].
def create_clusters(labels: np.array, items: List[MenuItem]) -> Dict[str, List[MenuItem]]:
    clusters: dict[str, list[MenuItem]] = {}
    for label, item in zip(labels, items):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(item)
    return clusters

# Create clusters using k-means algorithm.
# Create clusters from all the foods available in all cafe.
def clusters() -> Dict[str, List[MenuItem]]:
    items: list[MenuItem] = asyncio.run(DButils.get_all_items())
    data: list[list[float]] = numeric_foods(items)
    n: int = len(data)

    # Normaize the data
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(data)

    # Find the best number of clusters using silhouette score.
    scores: list = []
    for i in range(2, n+1):
        kmeans: KMeans = KMeans(n_clusters=i, random_state=42)
        scores.append(silhouette_score(normalized_data, kmeans.fit_predict(normalized_data)))
    max_score: float = max(scores)
    if Utilitaries.is_duplicated(max_score, scores):
        #TODO: Define an action to do to
        print("You need to choose")
    k: int = scores.index(max_score) + 1
    
    # Apply k-means
    kmeans: KMeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(normalized_data)
    clusters = create_clusters(kmeans.labels_, items)
    return clusters

# Update item's cluster in the database.
#TODO
def update_item_cluster():
    pass