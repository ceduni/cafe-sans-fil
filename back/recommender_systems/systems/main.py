### Code pour effectuer la fusion des recommandations ###
import collaborative_filtering as CF
import content_based_filtering as CBF
import knowledge_based as KBR
import global_recommendation as GR
import health_bot as HB

from typing import List, Dict
from app.models.cafe_model import MenuItem, Cafe
from app.models.user_model import User
import routines.food_clustering as Clustering
import recommender_systems.utils.utilitaries as Utilitaries
import asyncio

# This method takes the foods candidates by the algorihtms
#  and return the final recommandation.
def main(action: str) -> List[MenuItem]:
    clusters: dict[str, list[MenuItem]] = Clustering.clusters()
    users: list[User] = asyncio.run(Utilitaries.get_all_users())
    all_cafe: list[Cafe] = asyncio.run(Utilitaries.get_all_cafe())

    # Bot recommendations.
    bot_recommendations_set: set[MenuItem] = set()
    recs: list[str] = HB.main()
    for cafe in all_cafe:
        cafe_slug = cafe.slug
        bot_recommendations_set.add( asyncio.run(Utilitaries.get_items_from_slugs(recs, cafe_slug)) )
    bot_recommendations: list[MenuItem] = list(bot_recommendations_set)

    if action == "personnal":
        result = asyncio.run( personnal_recommendations(users, all_cafe, clusters) )
        result['healthy_recommendations'] = bot_recommendations
        return result
    elif action == "public":
        return bot_recommendations.extend(asyncio.run( Utilitaries.get_items_from_slugs(GR.main(cafe) ), cafe_slug))

#TODO
async def personnal_recommendations(users: List[User], list_cafe: List[Cafe], clusters: Dict[str, List[MenuItem]]) -> Dict[str, Dict[str, List[MenuItem]]]:
    recommendations: dict[str, dict[str, list[MenuItem]]] = {}
    for user in users:
        if user.id not in recommendations:
            cafes: dict[str, list[MenuItem]] = {}
            cf_recommendations: list[str] = CF.main(users, user)
            for cafe in list_cafe:
                cafe_slug: str = cafe.slug
                # Personnal recommendations.
                collab_filtering: list[MenuItem] = await Utilitaries.get_items_from_slugs(cf_recommendations, cafe_slug)
                content_based: list[MenuItem] = await Utilitaries.get_items_from_slugs(CBF.main(clusters, user, cafe), cafe_slug)
                knowledge_based: list[MenuItem] = await Utilitaries.get_items_from_slugs(KBR.main(cafe, user), cafe_slug)

                if cafe_slug not in cafes:
                    cafes[cafe_slug] = []

                cafes[cafe_slug].extend(collab_filtering)
                cafes[cafe_slug].extend(content_based)
                cafes[cafe_slug].extend(knowledge_based)
            
            recommendations[user.id] = cafes

    
    #TODO Define a proportion of recommendations.

    return recommendations