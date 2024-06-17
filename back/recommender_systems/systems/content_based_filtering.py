### Algorithme 4.2 ###
from app.services.user_service import UserService
from app.models.user_model import User
from app.models.cafe_model import MenuItem

import recommender_systems.routines.food_clustering as Clustering

# Take the clusters and the actual user as parameters and return the cluster
#  with the most likes.
def favorite_cluster(clusters, user):
    return

# Content based filtering algorithm.
# Recommend food based on the user consumption habits.
def algorithm(clusters: dict, user: User) -> list[MenuItem]:
    return

def main():
    clusters: dict = Clustering.clustering()
    user: User = any #TODO: Get the actual user
    algorithm(clusters, user)
    return