from fastapi import APIRouter, HTTPException
from typing import List
# from app.schemas.cafe_schema import CafeOut
# from app.services.search_service import search
from app.services.cafe_service import CafeService
search_router = APIRouter()

print("test")
@search_router.get("/search")
async def perform_search(query: str):
    try:
        # results = await search(query)
        # return results

        # Temporary using old search
        # To do: Fix and use new search
        filters = {}
        return await CafeService.search_cafes_and_items(query, **filters)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la recherche: {str(e)}")
