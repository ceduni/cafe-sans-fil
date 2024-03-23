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



# ###Verson 2  fonctionne avec items  seulement 
# from app.models.cafe_model import Cafe
# from typing import List, Dict, Any

# async def search(query: str, **filters) -> Dict[str, List[Any]]:
#     regex_pattern = {"$regex": query, "$options": "i"}
    
#     # plus ou moins le modele de cafe_service
#     for key in ['is_open', 'in_stock']:
#         if key in filters:
#             if filters[key].lower() == 'true':
#                 filters[key] = True
#             elif filters[key].lower() == 'false':
#                 filters[key] = False

#     # recherche dans les éléments de menu
#     item_query = {"menu_items": {"$elemMatch": {"name": regex_pattern}}}
#     item_query.update(filters)  
#     matching_cafes = await Cafe.find(item_query).to_list()

#    # uniquement les cafés contenant des éléments de menu correspondants
#     return {"matching_cafesssssss": matching_cafes}


###Version 3 , fonctionne avec items et cafes 
from app.models.cafe_model import Cafe
from typing import List, Dict, Any

async def search(query: str, **filters) -> Dict[str, List[Any]]:
    regex_pattern = {"$regex": query, "$options": "i"}

# plus ou moins le modele de cafe_service
    for key in ['is_open', 'in_stock']:
        if key in filters:
            if filters[key].lower() == 'true':
                filters[key] = True
            elif filters[key].lower() == 'false':
                filters[key] = False

    # Combinaison des search pour inclure les cafés par leur nom et par les éléments du menu
    combined_query = {
        "$or": [
            {"name": regex_pattern},  # search par nom du café
            {"menu_items": {"$elemMatch": {"name": regex_pattern}}}  # search dans les éléments de menu
        ]
    }
    combined_query.update(filters)  
    matching_cafes = await Cafe.find(combined_query).to_list()

    return {"matching_cafessss_and_items": matching_cafes}
