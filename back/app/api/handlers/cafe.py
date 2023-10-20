from fastapi import APIRouter, HTTPException, Depends, Query
from app.schemas.cafe_schema import Cafe, MenuItem
from app.services.cafe_service import CafeService
from uuid import UUID
from typing import List

cafe_router = APIRouter()

# --------------------------------------
#               Cafe
# --------------------------------------
@cafe_router.get("/cafes", response_model=List[Cafe])
async def list_cafes():
    return await CafeService.list_cafes()

@cafe_router.get("/cafes/{cafe_id}", response_model=Cafe)
async def get_cafe(cafe_id: UUID):
    cafe = await CafeService.retrieve_cafe(cafe_id)
    if not cafe:
        raise HTTPException(status_code=404, detail="Café not found")
    return cafe

@cafe_router.post("/cafes", response_model=Cafe)
async def create_cafe(cafe: Cafe):
    return await CafeService.create_cafe(cafe)

@cafe_router.put("/cafes/{cafe_id}", response_model=Cafe)
async def update_cafe(cafe_id: UUID, cafe: Cafe):
    return await CafeService.update_cafe(cafe_id, cafe)

# --------------------------------------
#               Menu
# --------------------------------------
@cafe_router.get("/cafes/{cafe_id}/menu", response_model=List[MenuItem])
async def list_menu_items(cafe_id: UUID):
    menu = await CafeService.retrieve_cafe_menu(cafe_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found for the given café.")
    return menu

@cafe_router.get("/cafes/{cafe_id}/menu/{item_id}", response_model=MenuItem)
async def get_menu_item(cafe_id: UUID, item_id: UUID):
    item = await CafeService.retrieve_menu_item(cafe_id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found.")
    return item

@cafe_router.post("/cafes/{cafe_id}/menu", response_model=MenuItem)
async def create_menu_item(cafe_id: UUID, item: MenuItem):
    return await CafeService.create_menu_item(cafe_id, item)

@cafe_router.put("/cafes/{cafe_id}/menu/{item_id}", response_model=MenuItem)
async def update_menu_item(cafe_id: UUID, item_id: UUID, item: MenuItem):
    return await CafeService.update_menu_item(cafe_id, item_id, item)

@cafe_router.delete("/cafes/{cafe_id}/menu/{item_id}", response_model=MenuItem)
async def delete_menu_item(cafe_id: UUID, item_id: UUID):
    try:
        deleted_item = await CafeService.delete_menu_item(cafe_id, item_id)
        return deleted_item
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# --------------------------------------
#               Search
# --------------------------------------
@cafe_router.get("/search")
async def unified_search(
    query: str = Query(..., description="Search query")):
    
    results = await CafeService.search_cafes_and_items(query)
    return results