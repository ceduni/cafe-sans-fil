"""
Module for handling category-related routes.
"""

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.cafe.menu.category.models import (
    MenuCategoryCreate,
    MenuCategoryOut,
    MenuCategoryUpdate,
)
from app.cafe.menu.category.service import CategoryService
from app.cafe.permissions import AdminPermission
from app.cafe.service import CafeService
from app.models import ErrorResponse

category_router = APIRouter()


@category_router.post(
    "/cafes/{slug}/menu/categories",
    response_model=MenuCategoryOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    dependencies=[Depends(AdminPermission())],
)
async def create_category(
    data: MenuCategoryCreate,
    slug: str = Path(..., description="Slug of the cafe"),
):
    """Create a menu category. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    category = await CategoryService.get_by_name(cafe, data.name)
    if category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[{"msg": "A category with this name already exists."}],
        )

    return await CategoryService.create(cafe, data)


@category_router.put(
    "/cafes/{slug}/menu/categories/{id}",
    response_model=MenuCategoryOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    dependencies=[Depends(AdminPermission())],
)
async def update_category(
    data: MenuCategoryUpdate,
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the category"),
):
    """Update a menu category. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    category = await CategoryService.get_by_id(cafe, id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A category with this ID does not exist."}],
        )

    category = await CategoryService.get_by_name(cafe, data.name)
    if category and category.id != id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[{"msg": "A category with this name already exists."}],
        )

    return await CategoryService.update(cafe, id, data)


@category_router.delete(
    "/cafes/{slug}/menu/categories/{id}",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    dependencies=[Depends(AdminPermission())],
)
async def delete_category(
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the category"),
):
    """Delete a menu category. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    category = await CategoryService.get_by_id(cafe, id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A category with this ID does not exist."}],
        )

    await CategoryService.delete(cafe, id)
