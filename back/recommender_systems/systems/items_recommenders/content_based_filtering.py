### Algorithme 4.2 ###
from app.models.user_model import User
from app.models.cafe_model import MenuItem, Cafe
from typing import List, Dict
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils

# Take the clusters and the actual user as parameters and return the cluster
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
            if user['user_id'] in item['likes']:
                tmp.append(item['slug'])
        n_likes.append((len(tmp), key))

    max_cluster: tuple[int, str] = max(n_likes) # Cluster with the most likes.
    res[max_cluster[1]] = clusters[max_cluster[1]]  
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

def algorithm(user: User, cafe_items: list[MenuItem], items_not_bought: set, number_recommendations: int = 10) -> List[str]:
    clusters: dict[str, list[MenuItem]] = Utilitaries.regroup_by_cluster(cafe_items)
    n = len(clusters)
    recommendations: list[MenuItem] = []

    # Find the k clusters with the most likes.
    try:
        favorit_clusters: list[list[MenuItem]] = []
        while len(favorit_clusters) < n:
            chosen_clusters: dict[str, list[MenuItem]] = favorite_cluster(clusters, user)
            favorit_clusters.append(list(chosen_clusters.values())[0])
            clusters: dict[str, list[MenuItem]] = remove_cluster(chosen_clusters, clusters)

        favorit_clusters_items_slugs: list[list[str]] = []
        for items in favorit_clusters:
            favorit_clusters_items_slugs.append(Utilitaries.items_slugs(items))

        for cluster in favorit_clusters_items_slugs:
            set_cluster: set = set(cluster)
            recommendations.extend( list( items_not_bought.intersection(set_cluster) ) ) # Items (not yet bought) in cafe and in most liked clusters.
    
    except ValueError as e:
        print(e)
        return []
    
    if number_recommendations > len(recommendations):
        k = len(recommendations)
    else:
        k = number_recommendations
    
    return list(set(recommendations))[:k]

# Content based filtering algorithm.
# Recommend food based on the user habits.
def main(user: User, cafe: Cafe, number_recommendations: int = 10) -> List[str]:
    if user is None or cafe is None:
        return []

    cafe_items = DButils.get_cafe_items(cafe['slug'])

    if isinstance(cafe_items, list) == False: # No item in the cafe.
        return []

    user_likes = DButils.get_user_likes_in_cafe(user['user_id'], cafe_items)
    items_not_bought: set = set(Utilitaries.items_not_bought_in_cafe(cafe, user))

    # At least one item in the cafe and the user has not liked any item.
    if len(user_likes) == 0 and len(cafe_items) > 0:
        return Utilitaries.most_liked_items(cafe_items)
    
    elif len(items_not_bought) == 0:
        return user_likes
    
    elif len(user_likes) > 0:
        return algorithm(user, cafe_items, items_not_bought, number_recommendations=number_recommendations)
