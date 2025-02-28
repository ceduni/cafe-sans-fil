"""
Module for handling menu-related routes.
"""

from typing import Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page
from pymongo.errors import DuplicateKeyError

from app.auth.dependencies import get_current_user
from app.cafe.menu.category.service import CategoryService
from app.cafe.menu.item.models import MenuItemCreate, MenuItemOut, MenuItemUpdate
from app.cafe.menu.item.service import ItemService
from app.cafe.models import Role
from app.cafe.service import CafeService
from app.models import ErrorConflictResponse, ErrorResponse
from app.service import parse_query_params
from app.user.models import User

item_router = APIRouter()


@item_router.get(
    "/cafes/{slug}/menu/items",
    response_model=Page[MenuItemOut],
    responses={
        404: {"model": ErrorResponse},
    },
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    filters = parse_query_params(dict(request.query_params))
    filters["cafe_id"] = cafe.id

    items = await ItemService.get_items(**filters)
    return await paginate(items)


@item_router.post(
    "/cafes/{slug}/menu/items",
    response_model=MenuItemOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorConflictResponse},
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    if data.category_id is not None:
        category = await CategoryService.get_category_by_id(cafe, data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[{"msg": "A category with this ID does not exist."}],
            )

    await CafeService.is_authorized_for_cafe_action(cafe, current_user, [Role.ADMIN])

    try:
        return await ItemService.create_item(cafe, data)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[
                {
                    "msg": "An item with these fields already exists.",
                    "fields": list(e.details.get("keyPattern", {}).keys()),
                }
            ],
        )


@item_router.get(
    "/cafes/{slug}/menu/items/{id}",
    response_model=MenuItemOut,
    responses={
        404: {"model": ErrorResponse},
    },
)
async def get_menu_item(
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the menu item"),
):
    """Get a menu item."""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    item = await ItemService.get_item_by_id_and_cafe_id(id, cafe.id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An item with this ID does not exist."}],
        )
    return item


@item_router.put(
    "/cafes/{slug}/menu/items/{id}",
    response_model=MenuItemOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorConflictResponse},
    },
)
async def update_menu_item(
    data: MenuItemUpdate,
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the menu item"),
    current_user: User = Depends(get_current_user),
):
    """Update a menu item. (`volunteer`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    item = await ItemService.get_item_by_id_and_cafe_id(id, cafe.id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An item with this ID does not exist."}],
        )

    if data.category_id is not None:
        category = await CategoryService.get_category_by_id(cafe, data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[{"msg": "A category with this ID does not exist."}],
            )

    await CafeService.is_authorized_for_cafe_action(
        cafe, current_user, [Role.ADMIN, Role.VOLUNTEER]
    )

    try:
        return await ItemService.update_item(item, data)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[
                {
                    "msg": "An item with these fields already exists.",
                    "fields": list(e.details.get("keyPattern", {}).keys()),
                }
            ],
        )


@item_router.delete(
    "/cafes/{slug}/menu/items/{id}",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def delete_menu_item(
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the menu item"),
    current_user: User = Depends(get_current_user),
):
    """Delete a menu item. (`admin`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    item = await ItemService.get_item_by_id_and_cafe_id(id, cafe.id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An item with this ID does not exist."}],
        )

    await CafeService.is_authorized_for_cafe_action(cafe, current_user, [Role.ADMIN])
    await ItemService.delete_item(item)
