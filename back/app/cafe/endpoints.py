"""
Module for handling cafe-related routes.
"""

from typing import Optional, TypeVar

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from fastapi_pagination import Params
from fastapi_pagination.customization import CustomizedPage, UseParams
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page
from pymongo.errors import DuplicateKeyError

from app.auth.dependencies import get_current_user, get_current_user_optional
from app.menu.models import MenuUpdate
from app.cafe.models import (
    CafeAggregateOut,
    CafeCreate,
    CafeOut,
    CafeShortOut,
    CafeUpdate,
)
from app.cafe.permissions import AdminPermission
from app.cafe.service import CafeService
from app.cafe.staff.enums import Role
from app.cafe.staff.service import StaffService
from app.models import ErrorConflictResponse, ErrorResponse
from app.service import parse_query_params
from app.user.models import User
from app.user.service import UserService

T = TypeVar("T")


class CafeParams(Params):
    """Custom pagination parameters."""

    size: int = Query(20, ge=1, le=100, description="Page size")
    page: int = Query(1, ge=1, description="Page number")
    sort_by: Optional[str] = Query(None, description="Sort by a specific field")
    is_open: Optional[bool] = Query(None, description="Filter by open status")


CafePage = CustomizedPage[
    Page[T],
    UseParams(CafeParams),
]


cafe_router = APIRouter()


@cafe_router.get(
    "/cafes",
    response_model=CafePage[CafeShortOut],
)
async def list_cafes(
    request: Request,
):
    """Get a list of cafes with basic information."""
    filters = parse_query_params(dict(request.query_params))
    cafes = await CafeService.get_all(to_list=False, **filters)
    return await paginate(cafes)

@cafe_router.get(
    "/cafes/{slug}",
    response_model=CafeAggregateOut,
    responses={
        404: {"model": ErrorResponse},
    },
)
async def get_cafe(
    slug: str = Path(..., description="Slug of the cafe"),
    current_user: User = Depends(get_current_user_optional),
):
    """Get a cafe with full details."""
    cafe = await CafeService.get(
        slug,
        aggregate=True,
        current_user_id=current_user.id if current_user else None,
    )
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
    dependencies=[Depends(AdminPermission())],
)
async def update_cafe(
    data: CafeUpdate,
    slug: str = Path(..., description="Slug of the cafe"),
    current_user: User = Depends(get_current_user),
):
    """Update a cafe. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    next_owner_id = PydanticObjectId(data.owner_id) if data.owner_id else None
    if next_owner_id:
        if next_owner_id != cafe.owner_id and current_user.id != cafe.owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=[{"msg": "You cannot change the owner of a cafe."}],
            )

        if not await StaffService.is_staff(cafe, next_owner_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=[{"msg": "The specified owner is not a staff member."}],
            )

        user = await UserService.get_by_id(next_owner_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[{"msg": "A user with this ID does not exist."}],
            )

        # Check if owner is changing
        if data.owner_id and data.owner_id != cafe.owner_id:
            # Update previous owner as admin
            await StaffService.add(cafe, Role.ADMIN, cafe.owner_id)

            # Remove previous role for new owner
            if data.owner_id in cafe.staff.admin_ids:
                await StaffService.remove(cafe, Role.ADMIN, data.owner_id)
            if data.owner_id in cafe.staff.volunteer_ids:
                await StaffService.remove(cafe, Role.VOLUNTEER, data.owner_id)

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


@cafe_router.put(
    "/cafes/{slug}/menu",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    dependencies=[Depends(AdminPermission())],
)
async def update_menu(
    data: MenuUpdate,
    slug: str = Path(..., description="Slug of the cafe"),
):
    """Update a cafe menu. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    await CafeService.update_menu(cafe, data)
