### Ce fichier contient les scripts qui permettront de créer des catégories de repas ###
from back.app.models.cafe_model import MenuItem
from recommender_systems.utils import utilitaries as Utilitaries

import asyncio

from collections import Counter
from typing import List, Dict, Any

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
    
# Check if a values is duplicated in a list.
def is_duplicated(element: Any, list: List[Any]) -> bool:
    counts = Counter(list)
    return counts[element] > 1

# Create clusters based on the labels got from kmeans.
# It assumes that the items in the 'items' and 'data' lists in the method 'clustering'
#   have the same indexing: items[i] equiv data[i].
def create_clusters(labels: np.array, items: List[MenuItem]) -> Dict[str, List[MenuItem]]:
    clusters = {}
    for label, item in zip(labels, items):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(item)
    return clusters

# Create clusters using k-means algorithm.
# Create clusters from all the foods available in all cafe.
def clusters() -> Dict[str, List[MenuItem]]:
    items: list[MenuItem] = asyncio.run(Utilitaries.get_all_items())
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
    if is_duplicated(max_score, scores):
        #TODO: Define an action to do to
        print("You need to choose")
    k: int = scores.index(max_score) + 1
    
    # Apply k-means
    kmeans: KMeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(normalized_data)
    clusters = create_clusters(kmeans.labels_, items)
    return clusters

#TODO
def assign_health_score(items: List[MenuItem]) -> List[MenuItem]:
    pass