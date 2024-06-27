### Algorithme 4.2 ###
from app.models.user_model import User
from app.models.cafe_model import MenuItem, Cafe
from typing import List, Dict, str
import recommender_systems.utils.utilitaries as Utilitaries
import numpy as np
from collections import Counter

# Take the clusters and the actual user as parameters and return the cluster/clusters
#  containing the most item the user liked.
# Note: The 'n_likes' indexing is the same indexing as 'clusters' dictionnary key's.
def favorite_cluster(clusters: Dict[str, List[MenuItem]], user: User) -> Dict[str, List[MenuItem]]:
    n_likes: list[int] = []
    res: dict[str, list[MenuItem]] = []
    # Get the number of likes per cluster.
    for key in clusters:
        tmp: list[MenuItem] = []
        for item in clusters[key]:
            if user.id in item.likes:
                tmp.append(item)
        n_likes.append(len(tmp))

    max_cluster = max(n_likes) # Cluster with the most likes.
    index = n_likes.index(max_cluster)
    res[str(index)] = clusters[str(index)]
    count = Counter(n_likes)
    if count[max_cluster] > 1:
        del clusters[str(index)]
        # Add all the clusters with same number of likes.
        for _ in range(count[max_cluster]-1):
            i = n_likes.index(max_cluster)
            res[str(i)] = clusters[str(i)]
            del clusters[str(i)]
    return res

# This method remove a specified cluster from the list of clusters.
def remove_cluster(chosen_clusters: Dict[str, List[MenuItem]], clusters: Dict[str, List[MenuItem]]):
    keys_to_remove = [key for key in clusters if key in chosen_clusters]
    
    for key in keys_to_remove:
        del clusters[key]

    return clusters

# Content based filtering algorithm.
# Recommend food based on the user habits.
async def main(clusters: Dict[str, List[MenuItem]], user: User, cafe: Cafe) -> List[str]:
    recommendations: list[MenuItem] = []
    items_not_bought: np.array[MenuItem] = np.array(await Utilitaries.meal_not_consumed(cafe, user))

    cafe_items: list[MenuItem] = cafe.menu_items
    # Number of clusters.
    if len(cafe_items) > 50:
        k: int = len(cafe_items)//3
    else:
        k: int = len(cafe_items)

    if len(items_not_bought) == 0:
        return user.likes[:k]

    # Find the k clusters with the most likes.
    favorit_clusters: list[list[MenuItem]] = []
    for _ in range(k):
        chosen_clusters: dict[str, list[MenuItem]] = favorite_cluster(clusters, user)
        favorit_clusters.extend(list(chosen_clusters.values()))
        clusters: dict[str, list[MenuItem]] = remove_cluster(chosen_clusters, clusters)
     
    for cluster in favorit_clusters:
        np_cluster: np.array[MenuItem] = np.array(cluster)
        np_cafe_items: np.array[MenuItem] = np.array(cafe_items)
        not_bought_cafe: np.array[MenuItem] = np.intersect1d(np_cafe_items, items_not_bought) # Items in cafe not yet bought.
        recommendations.extend(list( np.intersect1d(not_bought_cafe, np_cluster) )) # Items (not yet bought) in cafe and in most liked clusters.

    return Utilitaries.items_slugs( list( set(recommendations) ) )
