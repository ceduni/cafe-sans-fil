"""
Module for handling menu-related routes.
"""

from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status

from app.auth.dependencies import get_current_user
from app.cafe.models import Role
from app.cafe.service import CafeService
from app.cafe_menu.models import (
    MenuCategoryCreate,
    MenuCategoryOut,
    MenuCategoryUpdate,
    MenuItemCreate,
    MenuItemOut,
    MenuItemUpdate,
)
from app.cafe_menu.service import MenuService
from app.service import parse_query_params
from app.user.models import User

menu_router = APIRouter()


# --------------------------------------
#               Category
# --------------------------------------


@menu_router.post(
    "/cafes/{cafe_slug}/menu/categories",
    response_model=MenuCategoryOut,
)
async def create_menu_category(
    category_data: MenuCategoryCreate,
    cafe_slug: str = Path(..., description="Slug of the cafe"),
    current_user: User = Depends(get_current_user),
):
    """Create a menu category. (`admin`)"""
    # TODO: Implement authorization for staff
    cafe = await CafeService.get_cafe(cafe_slug)
    return await MenuService.create_menu_category(cafe.id, category_data)


@menu_router.put(
    "/cafes/{cafe_slug}/menu/categories/{category_id}",
    response_model=MenuCategoryOut,
)
async def update_menu_category(
    category_data: MenuCategoryUpdate,
    cafe_slug: str = Path(..., description="Slug of the cafe"),
    category_id: PydanticObjectId = Path(
        ..., description="ID of the category to update"
    ),
    current_user: User = Depends(get_current_user),
):
    """Update a menu category. (`admin`)"""
    # TODO: Implement authorization for staff
    cafe = await CafeService.get_cafe(cafe_slug)
    return await MenuService.update_menu_category(cafe.id, category_id, category_data)


@menu_router.delete(
    "/cafes/{cafe_slug}/menu/categories/{category_id}",
)
async def delete_menu_category(
    cafe_slug: str = Path(..., description="Slug of the cafe"),
    category_id: PydanticObjectId = Path(
        ..., description="ID of the category to delete"
    ),
    current_user: User = Depends(get_current_user),
):
    """Delete a menu category. (`admin`)"""
    # TODO: Implement authorization for staff
    cafe = await CafeService.get_cafe(cafe_slug)
    await MenuService.delete_menu_category(cafe.id, category_id)


# --------------------------------------
#               Item
# --------------------------------------


@menu_router.get(
    "/cafes/{cafe_slug}/menu/items",
    response_model=List[MenuItemOut],
)
async def get_menu_items(
    request: Request,
    cafe_slug: str = Path(..., description="The slug or ID of the cafe"),
    in_stock: Optional[bool] = Query(
        None, description="Filter menu items by stock availability (true/false)."
    ),
    sort_by: Optional[str] = Query(
        None,
        description="Sort menus by a specific field. Prefix with '-' for descending order (e.g., '-name').",
    ),
    page: Optional[int] = Query(
        1, description="Specify the page number for pagination."
    ),
    limit: Optional[int] = Query(
        40, description="Set the number of cafes to return per page."
    ),
) -> List[MenuItemOut]:
    """Get a list of menu items for a cafe."""
    query_params = dict(request.query_params)
    parsed_params = parse_query_params(query_params)

    cafe = await CafeService.get_cafe(cafe_slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cafe not found"
        )
    parsed_params["cafe_id"] = cafe.id

    return await MenuService.get_menu_items(**parsed_params)


@menu_router.post(
    "/cafes/{cafe_slug}/menu/items",
    response_model=MenuItemOut,
)
async def create_menu_item(
    item_data: MenuItemCreate,
    cafe_slug: str = Path(..., description="The slug or ID of the cafe"),
    current_user: User = Depends(get_current_user),
) -> MenuItemOut:
    """Create a menu item for a cafe. (`admin`)"""
    cafe = await CafeService.get_cafe(cafe_slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cafe not found"
        )

    try:
        await CafeService.is_authorized_for_cafe_action(
            cafe.id, current_user, [Role.ADMIN]
        )
        return await MenuService.create_menu_item(cafe.id, item_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@menu_router.get(
    "/cafes/{cafe_slug}/menu/items/{item_id}",
    response_model=MenuItemOut,
)
async def get_menu_item(
    item_id: PydanticObjectId = Path(..., description="The ID of the menu item"),
) -> MenuItemOut:
    """Get a menu item."""
    item = await MenuService.get_menu_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found."
        )
    return item


@menu_router.put(
    "/cafes/{cafe_slug}/menu/items/{item_id}",
    response_model=MenuItemOut,
)
async def update_menu_item(
    item_data: MenuItemUpdate,
    item_id: PydanticObjectId = Path(..., description="The ID of the menu item"),
    current_user: User = Depends(get_current_user),
) -> MenuItemOut:
    """Update a menu item. (`volunteer`)"""
    item = await MenuService.get_menu_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found."
        )

    try:
        await CafeService.is_authorized_for_cafe_action(
            item.cafe_id, current_user, [Role.ADMIN, Role.VOLUNTEER]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    try:
        updated_item = await MenuService.update_menu_item(item_id, item_data)
        return updated_item
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@menu_router.delete(
    "/cafes/{cafe_slug}/menu/items/{item_id}",
)
async def delete_menu_item(
    item_id: PydanticObjectId = Path(..., description="The ID of the menu item"),
    current_user: User = Depends(get_current_user),
):
    """Delete a menu item. (`admin`)"""
    item = await MenuService.get_menu_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found."
        )

    try:
        await CafeService.is_authorized_for_cafe_action(
            item.cafe_id, current_user, [Role.ADMIN]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    await MenuService.delete_menu_item(item_id)
    return {"message": f"Item {item_id} has been successfully deleted."}
