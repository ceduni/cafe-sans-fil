"""
Module for handling menu-related routes.
"""

from typing import Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

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
from app.models import ErrorResponse
from app.service import parse_query_params
from app.user.models import User

menu_router = APIRouter()


# --------------------------------------
#               Category
# --------------------------------------


@menu_router.post(
    "/cafes/{slug}/menu/categories",
    response_model=MenuCategoryOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def create_menu_category(
    data: MenuCategoryCreate,
    slug: str = Path(..., description="Slug of the cafe"),
    current_user: User = Depends(get_current_user),
):
    """Create a menu category. (`admin`)"""
    # TODO: Implement authorization for staff
    cafe = await CafeService.get(slug)
    return await MenuService.create_category(cafe, data)


@menu_router.put(
    "/cafes/{slug}/menu/categories/{id}",
    response_model=MenuCategoryOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def update_menu_category(
    data: MenuCategoryUpdate,
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the category"),
    current_user: User = Depends(get_current_user),
):
    """Update a menu category. (`admin`)"""
    # TODO: Implement authorization for staff
    cafe = await CafeService.get(slug)
    return await MenuService.update_category(cafe, id, data)


@menu_router.delete(
    "/cafes/{slug}/menu/categories/{id}",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def delete_menu_category(
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the category"),
    current_user: User = Depends(get_current_user),
):
    """Delete a menu category. (`admin`)"""
    # TODO: Implement authorization for staff
    cafe = await CafeService.get(slug)
    await MenuService.delete_category(cafe, id)


# --------------------------------------
#               Item
# --------------------------------------


@menu_router.get(
    "/cafes/{slug}/menu/items",
    response_model=Page[MenuItemOut],
)
async def get_menu_items(
    request: Request,
    slug: str = Path(..., description="Slug of the cafe"),
    in_stock: Optional[bool] = Query(None, description="Filter by stock availability"),
    sort_by: Optional[str] = Query(None, description="Sort by a specific field"),
):
    """Get a list of menu items for a cafe."""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cafe not found"
        )

    filters = parse_query_params(dict(request.query_params))
    filters["cafe_id"] = cafe.id

    items = await MenuService.get_items(**filters)
    return await paginate(items)


@menu_router.post(
    "/cafes/{slug}/menu/items",
    response_model=MenuItemOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def create_menu_item(
    data: MenuItemCreate,
    slug: str = Path(..., description="Slug of the cafe"),
    current_user: User = Depends(get_current_user),
):
    """Create a menu item for a cafe. (`admin`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cafe not found"
        )

    try:
        await CafeService.is_authorized_for_cafe_action(
            cafe, current_user, [Role.ADMIN]
        )
        return await MenuService.create_item(cafe, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@menu_router.get(
    "/cafes/{slug}/menu/items/{id}",
    response_model=MenuItemOut,
    responses={
        404: {"model": ErrorResponse},
    },
)
async def get_menu_item(
    id: PydanticObjectId = Path(..., description="ID of the menu item"),
):
    """Get a menu item."""
    item = await MenuService.get_item(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found."
        )
    return item


@menu_router.put(
    "/cafes/{slug}/menu/items/{id}",
    response_model=MenuItemOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def update_menu_item(
    data: MenuItemUpdate,
    id: PydanticObjectId = Path(..., description="ID of the menu item"),
    current_user: User = Depends(get_current_user),
):
    """Update a menu item. (`volunteer`)"""
    item = await MenuService.get_item(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found."
        )

    cafe = await CafeService.get(item.cafe_id)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cafe not found"
        )

    try:
        await CafeService.is_authorized_for_cafe_action(
            cafe, current_user, [Role.ADMIN, Role.VOLUNTEER]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    try:
        updated_item = await MenuService.update_item(item, data)
        return updated_item
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@menu_router.delete(
    "/cafes/{slug}/menu/items/{id}",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def delete_menu_item(
    id: PydanticObjectId = Path(..., description="ID of the menu item"),
    current_user: User = Depends(get_current_user),
):
    """Delete a menu item. (`admin`)"""
    item = await MenuService.get_item(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found."
        )

    cafe = await CafeService.get(item.cafe_id)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cafe not found"
        )

    try:
        await CafeService.is_authorized_for_cafe_action(
            cafe, current_user, [Role.ADMIN]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    await MenuService.delete_item(item)
    return {"message": f"Item {id} has been successfully deleted."}
