from fastapi import APIRouter, HTTPException, Query
from app.schemas.cafe_schema import CafeOut, CafeCreate, CafeUpdate, MenuItemOut, MenuItemCreate, MenuItemUpdate
from app.services.cafe_service import CafeService
from uuid import UUID
from typing import List

"""
This module defines the API routes related to cafes, their menus, and a unified search function for cafes and menu items.
"""

cafe_router = APIRouter()

# --------------------------------------
#               Cafe
# --------------------------------------

@cafe_router.get("/cafes", response_model=List[CafeOut])
async def list_cafes(is_open: bool = Query(None, description="Filter cafés based on open status"),
                     payment_method: str = Query(None, description="Filter cafés based on supported payment methods")):
    return await CafeService.list_cafes(is_open, payment_method)

@cafe_router.get("/cafes/{cafe_id}", response_model=CafeOut)
async def get_cafe(cafe_id: UUID):
    cafe = await CafeService.retrieve_cafe(cafe_id)
    if not cafe:
        raise HTTPException(status_code=404, detail="Café not found")
    return cafe

@cafe_router.post("/cafes", response_model=CafeOut)
async def create_cafe(cafe: CafeCreate):
    return await CafeService.create_cafe(cafe)

@cafe_router.put("/cafes/{cafe_id}", response_model=CafeOut)
async def update_cafe(cafe_id: UUID, cafe: CafeUpdate):
    return await CafeService.update_cafe(cafe_id, cafe)

# --------------------------------------
#               Menu
# --------------------------------------

@cafe_router.get("/cafes/{cafe_id}/menu", response_model=List[MenuItemOut])
async def list_menu_items(
    cafe_id: UUID, 
    category: str = Query(None, description="Filter menu items based on category"),
    is_available: bool = Query(None, description="Filter menu items based on availability")
):
    menu = await CafeService.list_menu_items(cafe_id, category, is_available)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found for the given café.")
    return menu

@cafe_router.get("/cafes/{cafe_id}/menu/{item_id}", response_model=MenuItemOut)
async def get_menu_item(cafe_id: UUID, item_id: UUID):
    item = await CafeService.retrieve_menu_item(cafe_id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found.")
    return item

@cafe_router.post("/cafes/{cafe_id}/menu",response_model=MenuItemOut)
async def create_menu_item(cafe_id: UUID, item: MenuItemCreate):
    return await CafeService.create_menu_item(cafe_id, item)

@cafe_router.put("/cafes/{cafe_id}/menu/{item_id}", response_model=MenuItemOut)
async def update_menu_item(cafe_id: UUID, item_id: UUID, item: MenuItemUpdate):
    return await CafeService.update_menu_item(cafe_id, item_id, item)

@cafe_router.delete("/cafes/{cafe_id}/menu/{item_id}")
async def delete_menu_item(cafe_id: UUID, item_id: UUID):
    try:
        deleted_item = await CafeService.delete_menu_item(cafe_id, item_id)
        return deleted_item
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# --------------------------------------
#               Search
# --------------------------------------

@cafe_router.get("/search", summary="Search for Cafes and Menu Items")
async def search(
    query: str = Query(..., description="Search query"),
    category: str = Query(None, description="Category to filter items by"),
    is_available: bool = Query(None, description="Filter items based on availability"),
    is_open: bool = Query(None, description="Filter cafés based on open status"),
    payment_method: str = Query(None, description="Filter cafés based on supported payment methods")):
    
    results = await CafeService.search_cafes_and_items(query, category, is_available, is_open, payment_method)
    return results