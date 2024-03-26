##Version 1 
# from typing import List
# from app.models.cafe_model import Cafe, MenuItem  

# # To fix
# @staticmethod
# async def search(query: str) -> List[Cafe]:
#     regex_pattern = f".*{query}.*"
#     regex_options = 'i'  
    
#     # Recherche des cafés dont les items de menu correspondent à la requête
#     matching_cafes = await Cafe.find(
#         Cafe.menu_items.any(MenuItem.name.match(regex_pattern, options=regex_options))
#     ).to_list()
    
#     return matching_cafes

###Version 2 , fonctionne avec items et cafes 
# from app.models.cafe_model import Cafe
# from typing import List, Dict, Any

# async def search(query: str, **filters) -> Dict[str, List[Any]]:
#     regex_pattern = {"$regex": query, "$options": "i"}

# # plus ou moins le modele de cafe_service
#     for key in ['is_open', 'in_stock']:
#         if key in filters:
#             if filters[key].lower() == 'true':
#                 filters[key] = True
#             elif filters[key].lower() == 'false':
#                 filters[key] = False

#     # Combinaison des search pour inclure les cafés par leur nom et par les éléments du menu
#     combined_query = {
#         "$or": [
#             {"name": regex_pattern},  # search par nom du café
#             {"menu_items": {"$elemMatch": {"name": regex_pattern}}}  # search dans les éléments de menu
#         ]
#     }
#     combined_query.update(filters)  
#     matching_cafes = await Cafe.find(combined_query).to_list()

#     return {"matching_cafessss_and_items": matching_cafes}

from app.models.cafe_model import Cafe
from typing import List, Dict, Any

async def search(query: str, **filters) -> Dict[str, List[Any]]:
    regex_pattern = {"$regex": query, "$options": "i"}

    for key in ['is_open', 'in_stock']:
        if key in filters:
            if filters[key].lower() == 'true':
                filters[key] = True
            elif filters[key].lower() == 'false':
                filters[key] = False

   # Combinaison des search pour inclure les cafés par leur nom et par les éléments du menu
    combined_query = {
        "$or": [
            {"name": regex_pattern},  
            {"menu_items": {"$elemMatch": {"name": regex_pattern}}} 
        ]
    }
    combined_query.update(filters)
    matching_cafes_full = await Cafe.find(combined_query).to_list()


    matching_cafes_and_items = []
    for cafe in matching_cafes_full:
        filtered_menu_items = [item for item in cafe.menu_items if query.lower() in item.name.lower()]

        
        cafe_dict = {
            "_id": str(cafe.id), 
            "cafe_id": str(cafe.cafe_id),
            "name": cafe.name,
            "slug": cafe.slug,
            "description": cafe.description,
            "image_url": cafe.image_url,
            "faculty": cafe.faculty,
            "is_open": cafe.is_open,
            "status_message": cafe.status_message,
            "opening_hours": cafe.opening_hours,
            "location": cafe.location,
            "contact": cafe.contact,
            "social_media": cafe.social_media,
            "payment_methods": cafe.payment_methods,
            "additional_info": cafe.additional_info,
            "menu_items": filtered_menu_items  
        }
        matching_cafes_and_items.append(cafe_dict)

    return {"matching_cafesssss_and_items": matching_cafes_and_items}
