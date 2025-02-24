"""
Module for handling search-related routes.
"""

from fastapi import APIRouter, HTTPException

from app.search.service import search

search_router = APIRouter()


@search_router.get("/search")
async def perform_search(query: str):
    """Search for cafes and menu items."""
    try:
        results = await search(query)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la recherche: {str(e)}"
        )
