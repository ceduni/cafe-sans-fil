### Code pour effectuer la fusion des recommandations ###
import collaborative_filtering as CF
import content_based_filtering as CBF
import knowledge_based as KBR
import global_recommendation as GR
import health_bot as HB

from typing import List, Dict
from app.models.cafe_model import MenuItem, Cafe
from app.models.user_model import User
from app.services.user_service import UserService
import routines.food_clustering as Clustering
import utilitaries as Utilitaries

# This method takes the foods candidates by the algorihtms
#  and return the final recommandation.
async def main(action: str, n: int) -> List[MenuItem]:
    clusters: dict[str, list[MenuItem]] = Clustering.clusters()
    user: User #TODO: Get the actual user.
    users: list[User] #TODO: Get all users.
    cafe: Cafe #TODO: Get the actual cafe.
    cafe_slug: str = cafe.slug

    # Bot recommendations.
    health_bot_recommendations: list[MenuItem] = await Utilitaries.get_items_from_slugs(HB.main(), cafe_slug)

    if action == "personnal":
        return await health_bot_recommendations.extend(personnal_recommendations(user, users, cafe, clusters, n))
    elif action == "public":
        return await health_bot_recommendations.extend(Utilitaries.get_items_from_slugs(GR.main(cafe), cafe_slug))

#TODO
async def personnal_recommendations(user: User, users: List[User], cafe: Cafe, clusters: Dict[str, List[MenuItem]], n : int) -> List[MenuItem]:
    cafe_slug: str = cafe.slug
    # Personnal recommendations.
    collab_filtering: list[MenuItem] = await Utilitaries.get_items_from_slugs(CF.main(users, user), cafe_slug)
    content_based: list[MenuItem] = await Utilitaries.get_items_from_slugs(CBF.main(clusters, user, cafe), cafe_slug)
    knowledge_based: list[MenuItem] = await Utilitaries.get_items_from_slugs(KBR.main(cafe, user), cafe_slug)

    #TODO Define a proportion of recommendations.

    return
