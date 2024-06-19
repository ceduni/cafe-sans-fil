### Code pour effectuer la fusion des recommandations ###
import collaborative_filtering as CF
import content_based_filtering as CBF
import knowledge_based as KBR
import global_recommendation as GR
import health_bot as HB

from typing import List
from app.models.cafe_model import MenuItem, Cafe
from app.models.user_model import User
import routines.food_clustering as Clustering


# This method takes the foods candidates by the algorihtms
#  and return the final recommandation.
def main(n_recommendations: int) -> List[MenuItem]:
    clusters: dict[str, list[MenuItem]] = Clustering.clusters()
    user: User #TODO: Get the actual user.
    users: list[User] #TODO: Get all users.
    cafe: Cafe #TODO: Get the actual cafe.



    return
