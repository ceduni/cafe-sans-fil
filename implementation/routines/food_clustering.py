### Ce fichier contient les scripts qui permettront de créer des catégories de repas ###
from back.app.services.cafe_service import CafeService
from back.app.models.cafe_model import Cafe, MenuItem
import asyncio

import itertools
from collections import Counter

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Get items/foods from the database
async def get_foods_db() -> list[MenuItem]:
    query_params = {
        "page": 1,
        "limit": 40,
        "sort_by": "name"
    }
    cafes: list[Cafe] = await CafeService.list_cafes(**query_params)
    items: list[list[MenuItem]] = list(map(lambda x: x.menu_items, cafes))
    return list(itertools.chain(*items))


def numeric_foods(foods: list[MenuItem]) -> list[any]:
    #TODO: Find the attributes of the foods necessary to transform them into numeric
    # values without losing the similarity between them (nutritionnal values for exemple)
    pass

# Check if a values is duplicated in a list.
def is_duplicated(element: any, list: list[any]) -> bool:
    counts = Counter(list)
    return counts[element] > 1

# Create clusters based on the labels got from kmeans.
# It assumes that the items in the 'items' and 'data' lists in the method 'clustering'
#   have the same indexing: items[i] equiv data[i].
def create_clusters(labels: np.array, items: list[MenuItem]) -> dict:
    clusters = {}
    for label, item in zip(labels, items):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(item)
    return clusters

# Create clusters using k-means algorithm.
# Create clusters from all the foods available in all cafe.
def clustering() -> dict:
    items: list[MenuItem] = asyncio.run(get_foods_db())
    data: list[any] = numeric_foods(items) #TODO: update the type of the list
    n: int = len(data)

    # Find the best number of clusters using silhouette score.
    scores: list = []
    for i in range(1, n+1):
        kmeans: KMeans = KMeans(n_clusters=i, random_state=42)
        scores.append(silhouette_score(data, kmeans.fit_predict(data)))
    max_score: float = max(scores)
    if is_duplicated(max_score, scores):
        #TODO: Define an action to do to
        print("You need to choose")
    k: int = scores.index(max_score) + 1
    
    # Apply k-means
    kmeans: KMeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data)
    clusters = create_clusters(kmeans.labels_, items)
    return clusters