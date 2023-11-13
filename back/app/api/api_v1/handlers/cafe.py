from fastapi import APIRouter, HTTPException, Query, Depends
from app.schemas.cafe_schema import CafeOut, CafeCreate, CafeUpdate, MenuItemOut, MenuItemCreate, MenuItemUpdate, Role
from app.services.cafe_service import CafeService
from uuid import UUID
from typing import List
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user

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
async def create_cafe(cafe: CafeCreate, current_user: User = Depends(get_current_user)):
    return await CafeService.create_cafe(cafe)

@cafe_router.put("/cafes/{cafe_id}", response_model=CafeOut)
async def update_cafe(cafe_id: UUID, cafe: CafeUpdate, current_user: User = Depends(get_current_user)):
    cafe_exists = await CafeService.retrieve_cafe(cafe_id)
    if not cafe_exists:
        raise HTTPException(status_code=404, detail="Café not found")

    try:
        await CafeService.is_authorized_for_cafe_action(cafe_id, current_user, [Role.ADMIN])
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=404, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=403, detail=str(e))

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

@cafe_router.post("/cafes/{cafe_id}/menu", response_model=MenuItemOut)
async def create_menu_item(cafe_id: UUID, item: MenuItemCreate, current_user: User = Depends(get_current_user)):
    try:
        await CafeService.is_authorized_for_cafe_action(cafe_id, current_user, [Role.ADMIN])
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=404, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=403, detail=str(e))

    return await CafeService.create_menu_item(cafe_id, item)

@cafe_router.put("/cafes/{cafe_id}/menu/{item_id}", response_model=MenuItemOut)
async def update_menu_item(cafe_id: UUID, item_id: UUID, item: MenuItemUpdate, current_user: User = Depends(get_current_user)):
    try:
        await CafeService.is_authorized_for_cafe_action(cafe_id, current_user, [Role.ADMIN])
        return await CafeService.update_menu_item(cafe_id, item_id, item)
    except ValueError as e:
        error_message = str(e)
        if error_message == "Menu item not found":
            raise HTTPException(status_code=404, detail=error_message)
        elif error_message == "Cafe not found":
            raise HTTPException(status_code=404, detail=error_message)
        elif error_message == "Access forbidden":
            raise HTTPException(status_code=403, detail=error_message)

@cafe_router.delete("/cafes/{cafe_id}/menu/{item_id}")
async def delete_menu_item(cafe_id: UUID, item_id: UUID, current_user: User = Depends(get_current_user)):
    try:
        await CafeService.is_authorized_for_cafe_action(cafe_id, current_user, [Role.ADMIN])
        await CafeService.delete_menu_item(cafe_id, item_id)
        return {"message": f"Item has been successfully deleted."}
    except ValueError as e:
        error_message = str(e)
        if error_message == "Menu item not found":
            raise HTTPException(status_code=404, detail=error_message)
        elif error_message == "Cafe not found":
            raise HTTPException(status_code=404, detail=error_message)
        elif error_message == "Access forbidden":
            raise HTTPException(status_code=403, detail=error_message)
    
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
