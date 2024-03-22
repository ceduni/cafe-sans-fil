from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.cafe_schema import CafeOut
from app.services.search_service import search

search_router = APIRouter()

print("test")
@search_router.get("/search", response_model=List[CafeOut])
async def perform_search(query: str):
    try:
        results = await search(query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la recherche: {str(e)}")
