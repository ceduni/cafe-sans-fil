"""
Module for handling item-related routes.
"""

from typing import Optional, TypeVar

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from fastapi_pagination import Params
from fastapi_pagination.customization import CustomizedPage, UseParams
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page
from pymongo.errors import DuplicateKeyError

from app.menu.category.service import CategoryService
from app.menu.item.models import MenuItemCreate, MenuItemOut, MenuItemUpdate
from app.menu.item.service import ItemService
from app.cafe.permissions import AdminPermission, VolunteerPermission
from app.cafe.service import CafeService
from app.models import ErrorConflictResponse, ErrorResponse
from app.service import parse_query_params

T = TypeVar("T")


class ItemParams(Params):
    """Custom pagination parameters."""

    size: int = Query(20, ge=1, le=100, description="Page size")
    page: int = Query(1, ge=1, description="Page number")
    sort_by: Optional[str] = Query(None, description="Sort by a specific field")
    in_stock: Optional[bool] = Query(None, description="Filter by stock availability")


ItemPage = CustomizedPage[
    Page[T],
    UseParams(ItemParams),
]


item_router = APIRouter()


@item_router.get(
    "/cafes/{slug}/menu/items",
    response_model=ItemPage[MenuItemOut],
    responses={
        404: {"model": ErrorResponse},
    },
)
async def list_items(
    request: Request,
    slug: str = Path(..., description="Slug of the cafe"),
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

    items = await ItemService.get_all(to_list=False, **filters)
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
    dependencies=[Depends(AdminPermission())],
)
async def create_item(
    data: MenuItemCreate,
    slug: str = Path(..., description="Slug of the cafe"),
):
    """Create a menu item for a cafe. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    if data.category_ids is not None:
        for category_id in data.category_ids:
            category = await CategoryService.get_by_id(cafe, category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=[
                        {
                            "msg": "A category with this ID does not exist.",
                            "id": str(category_id),
                        }
                    ],
                )

    try:
        return await ItemService.create(cafe, data)
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
async def get_item(
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

    item = await ItemService.get_by_id_and_cafe_id(id, cafe.id)
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
    dependencies=[Depends(VolunteerPermission())],
)
async def update_item(
    data: MenuItemUpdate,
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the menu item"),
):
    """Update a menu item. (`VOLUNTEER`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    item = await ItemService.get_by_id_and_cafe_id(id, cafe.id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An item with this ID does not exist."}],
        )

    if data.category_ids is not None:
        for category_id in data.category_ids:
            category = await CategoryService.get_by_id(cafe, category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=[
                        {
                            "msg": "A category with this ID does not exist.",
                            "id": str(category_id),
                        }
                    ],
                )

    try:
        return await ItemService.update(item, data)
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
    dependencies=[Depends(AdminPermission())],
)
async def delete_item(
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the menu item"),
):
    """Delete a menu item. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    item = await ItemService.get_by_id_and_cafe_id(id, cafe.id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An item with this ID does not exist."}],
        )

    await ItemService.delete(item)
