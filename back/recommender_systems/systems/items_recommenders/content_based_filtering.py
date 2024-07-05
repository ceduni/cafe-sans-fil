### Algorithme 4.2 ###
from app.models.user_model import User
from app.models.cafe_model import MenuItem, Cafe
from typing import List, Dict
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils
import numpy as np
from collections import Counter

# Take the clusters and the actual user as parameters and return the cluster/clusters
#  containing the most item the user liked.
# Note: The 'n_likes' indexing is the same indexing as 'clusters' dictionnary keys.
def favorite_cluster(clusters: Dict[str, List[MenuItem]], user: User) -> Dict[str, List[MenuItem]]:
    if len(clusters) == 0 or clusters is None:
        raise ValueError('Clusters cannot be empty or None')
    
    if user is None:
        raise ValueError('User cannot be None')

    # Get the number of likes per cluster.
    n_likes: list[tuple[int, str]] = []
    res: dict[str, list[MenuItem]] = {}
    # Get the number of likes per cluster.
    for key in clusters:
        tmp: list[MenuItem] = []
        for item in clusters[key]:
            if user['id'] in item['likes']:
                tmp.append(item['slug'])
        n_likes.append((len(tmp), key))

    max_cluster: tuple[int, str] = max(n_likes) # Cluster with the most likes.
    max_value: int = max_cluster[0]
    res[max_cluster[1]] = clusters[max_cluster[1]]
    del clusters[str(max_cluster[1])]
    n_likes.remove(max_cluster)

    stop = False
    while not stop:
        if max(n_likes)[0] == max_value:
            max_cluster = max(n_likes)
            res[max_cluster[1]] = clusters[max_cluster[1]]
            del clusters[str(max_cluster[1])]
            n_likes.remove(max_cluster)
        else:
            stop = True     
    return res

# This method remove a specified clusters from the list of clusters.
def remove_cluster(chosen_clusters: Dict[str, List[MenuItem]], clusters: Dict[str, List[MenuItem]]):
    if len(clusters) == 0 or clusters is None:
        raise ValueError("Clusters are empty or there is no clusters.")

    if len(chosen_clusters) == 0 or chosen_clusters is None:
        return clusters

    keys_to_remove = [key for key in clusters if key in chosen_clusters]
    
    for key in keys_to_remove:
        del clusters[key]

    return clusters

def algorithm(user: User, cafe: Cafe, items_not_bought: set) -> List[str]:
    cafe_items: list[MenuItem] = cafe['menu_items']
    clusters: dict[str, list[str]] = Utilitaries.regroup_by_cluster(cafe_items)
    recommendations: list[MenuItem] = []

    # Number of clusters.
    if len(cafe_items) > 50:
        k: int = len(cafe_items)//3
    else:
        k: int = len(cafe_items)

    # Find the k clusters with the most likes.
    try:
        favorit_clusters: list[list[str]] = []
        for _ in range(len(clusters)):
            chosen_clusters: dict[str, list[str]] = favorite_cluster(clusters, user)
            favorit_clusters.extend(list(chosen_clusters.values()))
            clusters: dict[str, list[MenuItem]] = remove_cluster(chosen_clusters, clusters)
        for cluster in favorit_clusters:
            set_cluster: set = set(cluster)
            recommendations.extend( list( items_not_bought.intersection(set_cluster) ) ) # Items (not yet bought) in cafe and in most liked clusters.
    except ValueError as e:
        print(e)
        return []
    
    return list(set(recommendations))[:k]

# Content based filtering algorithm.
# Recommend food based on the user habits.
def main(user: User, cafe: Cafe) -> List[str]:
    if user is None or cafe is None or len(cafe['menu_items']) == 0:
        return []
    else:
        user_likes = DButils.get_user_likes(user['id'])
        items_not_bought: set = set(Utilitaries.meal_not_consumed(cafe, user))
        # At least one item in the cafe and the user has not liked any item.
        if len(user_likes) == 0 and len(cafe['menu_items']) > 0:
            return Utilitaries.most_liked_items(cafe['menu_items'])
        
        elif len(items_not_bought) == 0:
            return user_likes
        
        elif len(user_likes) > 0:
            return algorithm(user, cafe, items_not_bought)

