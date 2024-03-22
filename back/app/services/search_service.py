from typing import List
from app.models.cafe_model import Cafe, MenuItem  

# To fix
@staticmethod
async def search(query: str) -> List[Cafe]:
    regex_pattern = f".*{query}.*"
    regex_options = 'i'  
    
    # Recherche des cafés dont les items de menu correspondent à la requête
    matching_cafes = await Cafe.find(
        Cafe.menu_items.any(MenuItem.name.match(regex_pattern, options=regex_options))
    ).to_list()
    
    return matching_cafes
