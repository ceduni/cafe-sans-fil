from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from tqdm import tqdm
from app.models.user_model import User
from recommender_systems.utils import db_utils as DButils
from recommender_systems.utils.utilitaries import create_clusters, find_indexes, list_items
from typing import List, Dict
from recommender_systems.utils.api_calls import UserApi, AuthApi

def _get_users() -> List[User]:
    return DButils.get_all_users()

def preprocess(users : List[User]) -> List[List[str]]:
    users_infos: List[str] = []
    for _, user in enumerate(tqdm(users, desc="Preprocessing")):
        user_infos = []
        user_infos.extend( list_items( DButils.get_user_orders(user) ) )
        user_infos.extend( DButils.get_all_user_likes(user['username']) )
        user_infos.extend( DButils.get_user_visited_cafe(user) )
        print(user_infos)
        users_infos.append(" ".join(items) for items in user_infos)
    
    print(users_infos)

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(users_infos)
    return X


def _clustering() -> Dict[str, List[User]]:
    users: List[User] = _get_users()
    X = preprocess(users)
    scores: list[float] = []
    for _, i in enumerate( tqdm(range(2, len(X)-1), desc="Finding best number of clusters") ):
        kmeans = KMeans(n_clusters=i, random_state=40).fit(X)
        scores.append(silhouette_score(X, kmeans.fit_predict(X)))
    max_score: float = max(scores)
    indexes: list[int] = find_indexes(scores, max_score)
    if len(indexes) > 1:
        k: int = scores[max(indexes)] + 1
    else: 
        k: int = scores.index(max_score) + 1
    
    kmeans = KMeans(n_clusters=k, random_state=40).fit(X)

    try:
        clusters = create_clusters(kmeans.labels_, users)
    except ValueError as e:
        print(e)
        clusters = {}

    return clusters

def update_user_cluster() -> None:
    clusters = _clustering()
    for _, cluster in enumerate(tqdm(clusters.keys(), desc="Updating users clusters")):
        for user in clusters[cluster]:
            data = {
                'cluster': cluster
            }
            UserApi.update_user(AuthApi.auth_login(), user['username'], json_data=data)