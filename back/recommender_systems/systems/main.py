### Code pour effectuer la fusion des recommandations ###
import collaborative_filtering as CF
import content_based_filtering as CBF
import knowledge_based as KBR
import global_recommendation as GR
import health_bot as HB

from typing import List, Dict, Union
from app.models.cafe_model import MenuItem, Cafe
from app.models.user_model import User
import back.recommender_systems.routines.routines as Clustering
import recommender_systems.utils.utilitaries as Utilitaries
import asyncio

#TODO: define a number of recommendations
# This method takes the foods candidates by the algorihtms
#  and return the final recommandation.
def main(action: str) -> Union[Dict[str, List[str]], Dict[str, Dict[str, List[str]]]]:
    clusters: dict[str, list[MenuItem]] = Clustering.clusters()
    users: list[User] = asyncio.run(Utilitaries.get_all_users())
    all_cafe: list[Cafe] = asyncio.run(Utilitaries.get_all_cafe())

    # Bot recommendations.
    bot_recommendations: dict[str, list[str]] = HB.main(all_cafe)

    if action == "bot":
        return bot_recommendations
    elif action == "personnal":
        result: dict[str, dict[str, list[str]]] = asyncio.run( personnal_recommendations(users, all_cafe, clusters) )
        return result
    elif action == "public":
        public_recommendations: dict[str, list[str]] = {}
        for cafe in all_cafe:
            cafe_slug = cafe.slug
            if cafe_slug not in public_recommendations:
                public_recommendations[cafe_slug] = []
            public_recommendations[cafe_slug].extend( asyncio.run(Utilitaries.filter_items_by_cafe(GR.main(cafe)), cafe_slug) )
        return public_recommendations

#TODO
async def personnal_recommendations(users: List[User], list_cafe: List[Cafe], clusters: Dict[str, List[MenuItem]]) -> Dict[str, Dict[str, List[str]]]:
    recommendations: dict[str, dict[str, list[str]]] = {}
    for user in users:
        if user.id not in recommendations:
            cafes: dict[str, list[str]] = {}
            cf_recommendations: list[str] = CF.main(users, user)
            for cafe in list_cafe:
                cafe_slug: str = cafe.slug
                # Personnal recommendations.
                collab_filtering: list[str] = await Utilitaries.filter_items_by_cafe(cf_recommendations, cafe_slug)
                content_based: list[str] = await Utilitaries.filter_items_by_cafe(CBF.main(clusters, user, cafe), cafe_slug)
                knowledge_based: list[str] = await Utilitaries.filter_items_by_cafe(KBR.main(cafe, user), cafe_slug)

                if cafe_slug not in cafes:
                    cafes[cafe_slug] = []

                cafes[cafe_slug].extend(collab_filtering)
                cafes[cafe_slug].extend(content_based)
                cafes[cafe_slug].extend(knowledge_based)
            
            recommendations[user.id] = cafes

    
    #TODO Define a proportion ofr recommendations.

    return recommendations
