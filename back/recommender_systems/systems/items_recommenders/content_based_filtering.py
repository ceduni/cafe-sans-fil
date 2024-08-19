from app.models.user_model import User
from app.models.cafe_model import MenuItem, Cafe
from typing import List, Dict, Tuple
from recommender_systems.utils import utilitaries as Utilitaries, db_utils as DButils

# Take the clusters and the actual user as parameters and return the cluster
# containing the most items the user liked, along with the count of likes.
def favorite_cluster(clusters: Dict[str, List[MenuItem]], user: User) -> Tuple[str, List[Tuple[str, int]]]:
    if len(clusters) == 0 or clusters is None:
        raise ValueError('Clusters cannot be empty or None')
    
    if user is None:
        raise ValueError('User cannot be None')

    # Get the number of likes per cluster.
    n_likes: List[Tuple[int, str]] = []
    cluster_likes: Dict[str, List[Tuple[str, int]]] = {}

    for key in clusters:
        tmp: List[Tuple[str, int]] = []
        for item in clusters[key]:
            likes_count = item['likes'].count(user['user_id'])
            if likes_count > 0:
                tmp.append((item['slug'], likes_count))
        n_likes.append((len(tmp), key))
        cluster_likes[key] = tmp

    max_cluster: Tuple[int, str] = max(n_likes)  # Cluster with the most likes.
    return max_cluster[1], cluster_likes[max_cluster[1]]

# This method removes a specified cluster from the list of clusters.
def remove_cluster(chosen_cluster_key: str, clusters: Dict[str, List[MenuItem]]) -> Dict[str, List[MenuItem]]:
    if len(clusters) == 0 or clusters is None:
        raise ValueError("Clusters are empty or there are no clusters.")

    if chosen_cluster_key in clusters:
        del clusters[chosen_cluster_key]

    return clusters

def algorithm(user: User, cafe_items: List[MenuItem], items_not_bought: set, number_recommendations: int = 10) -> List[Tuple[str, int]]:
    clusters: Dict[str, List[MenuItem]] = Utilitaries.regroup_by_cluster(cafe_items)
    n = len(clusters)
    recommendations: List[Tuple[str, int]] = []

    # Find the k clusters with the most likes.
    try:
        favorit_clusters: List[List[Tuple[str, int]]] = []
        while len(favorit_clusters) < n:
            chosen_cluster_key, chosen_cluster = favorite_cluster(clusters, user)
            favorit_clusters.append(chosen_cluster)
            clusters = remove_cluster(chosen_cluster_key, clusters)

        for cluster in favorit_clusters:
            #set_cluster = {item for item, _ in cluster}
            for item, likes_count in cluster:
                if item in items_not_bought:
                    recommendations.append((item, likes_count))

    except ValueError as e:
        print(e)
        return []
    
    if number_recommendations > len(recommendations):
        k = len(recommendations)
    else:
        k = number_recommendations
    
    return recommendations[:k]

# Content-based filtering algorithm.
# Recommend food based on the user's habits.
def main(user: User, cafe: Cafe, number_recommendations: int = 10) -> Dict[str, int]:
    if user is None or cafe is None:
        return []

    cafe_items = DButils.get_cafe_items(cafe['slug'])

    if not isinstance(cafe_items, list):  # No item in the cafe.
        return []

    user_likes = DButils.get_user_likes_in_cafe(user['user_id'], cafe_items)
    items_not_bought: set = set(Utilitaries.items_not_bought_in_cafe(cafe, user))

    # At least one item in the cafe, and the user has not liked any item.
    if len(user_likes) == 0 and len(cafe_items) > 0:
        return Utilitaries.format_recommendation_output( Utilitaries.most_liked_items(cafe_items) )

    elif len(items_not_bought) == 0:
        tuples: List[Tuple[str, int]] =[(item['slug'], 1) for item in user_likes]
        return Utilitaries.format_recommendation_output(tuples)
    
    elif len(user_likes) > 0:
        return Utilitaries.format_recommendation_output( algorithm(user, cafe_items, items_not_bought, number_recommendations=number_recommendations) )
