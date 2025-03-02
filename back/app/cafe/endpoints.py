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

from app.auth.dependencies import get_current_user
from app.cafe.models import CafeCreate, CafeOut, CafeShortOut, CafeUpdate, CafeViewOut
from app.cafe.permissions import AdminPermission
from app.cafe.service import CafeService
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
async def get_cafes(
    request: Request,
):
    """Get a list of cafes with basic information."""
    filters = parse_query_params(dict(request.query_params))
    cafes = await CafeService.get_all(to_list=False, **filters)
    return await paginate(cafes)


@cafe_router.post(
    "/cafes",
    response_model=CafeOut,
    responses={
        401: {"model": ErrorResponse},
        409: {"model": ErrorConflictResponse},
    },
)
async def create_cafe(
    data: CafeCreate,
    current_user: User = Depends(get_current_user),
):
    """Create a cafe. (`MEMBER`)"""
    try:
        return await CafeService.create(data, current_user.id)
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
