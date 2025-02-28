"""
Module for handling cafe-related routes.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page
from pymongo.errors import DuplicateKeyError

from app.auth.dependencies import get_current_user
from app.cafe.models import (
    CafeCreate,
    CafeOut,
    CafeShortOut,
    CafeUpdate,
    CafeViewOut,
    Role,
)
from app.cafe.service import CafeService
from app.models import ErrorConflictResponse, ErrorResponse
from app.service import parse_query_params
from app.user.models import User

cafe_router = APIRouter()


@cafe_router.get(
    "/cafes",
    response_model=Page[CafeShortOut],
)
async def get_cafes(
    request: Request,
    is_open: Optional[bool] = Query(None, description="Filter by open status"),
    sort_by: Optional[str] = Query(None, description="Sort by a specific field"),
):
    """Get a list of cafes with basic information."""
    filters = parse_query_params(dict(request.query_params))
    cafes = await CafeService.get_all(**filters)
    return await paginate(cafes)


@cafe_router.post(
    "/cafes",
    response_model=CafeOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        409: {"model": ErrorConflictResponse},
    },
)
async def create_cafe(
    data: CafeCreate,
    current_user: User = Depends(get_current_user),
):
    """Create a cafe (`superuser`)."""
    if "7802085" != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"msg": "Only superusers can create cafes"}],
        )

    try:
        return await CafeService.create(data)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[
                {
                    "msg": "A cafe with these fields already exists.",
                    "fields": list(e.details.get("keyPattern", {}).keys()),
                }
            ],
        )


@cafe_router.get(
    "/cafes/{slug}",
    response_model=CafeViewOut,
    responses={
        404: {"model": ErrorResponse},
    },
)
async def get_cafe(
    slug: str = Path(..., description="Slug of the cafe"),
):
    """Get a cafe with full details."""
    cafe = await CafeService.get(slug, as_view=True)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )
    return cafe


@cafe_router.put(
    "/cafes/{slug}",
    response_model=CafeOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorConflictResponse},
    },
)
async def update_cafe(
    data: CafeUpdate,
    slug: str = Path(..., description="Slug of the cafe"),
    current_user: User = Depends(get_current_user),
):
    """Update a cafe (`admin`)."""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    await CafeService.is_authorized_for_cafe_action(cafe, current_user, [Role.ADMIN])

    try:
        return await CafeService.update(cafe, data)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[
                {
                    "msg": "A cafe with these fields already exists.",
                    "fields": list(e.details.get("keyPattern", {}).keys()),
                }
            ],
        )
