"""
Module for handling announcement-related routes.
"""

from typing import Optional, TypeVar

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from fastapi_pagination import Params
from fastapi_pagination.customization import CustomizedPage, UseParams
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

from app.auth.dependencies import get_current_user
from app.cafe.announcement.models import (
    AnnouncementAggregateOut,
    AnnouncementCreate,
    AnnouncementOut,
    AnnouncementUpdate,
)
from app.cafe.announcement.service import AnnouncementService
from app.cafe.permissions import AdminPermission
from app.cafe.service import CafeService
from app.models import ErrorResponse
from app.service import parse_query_params
from app.user.models import User

T = TypeVar("T")


class AnnouncementParams(Params):
    """Custom pagination parameters."""

    size: int = Query(20, ge=1, le=100, description="Page size")
    page: int = Query(1, ge=1, description="Page number")
    sort_by: Optional[str] = Query(None, description="Sort by a specific field")
    cafe_id: Optional[PydanticObjectId] = Query(None, description="Filter by cafe ID")


AnnouncementPage = CustomizedPage[
    Page[T],
    UseParams(AnnouncementParams),
]


announcement_router = APIRouter()


@announcement_router.get(
    "/announcements/",
    response_model=AnnouncementPage[AnnouncementAggregateOut],
)
async def list_announcements(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    """Get a list of announcements."""
    filters = parse_query_params(dict(request.query_params))
    announcements = await AnnouncementService.get_all(
        to_list=False,
        aggregate=True,
        current_user_id=current_user.id,
        **filters,
    )
    return await paginate(announcements)


@announcement_router.post(
    "/cafes/{slug}/announcements/",
    response_model=AnnouncementOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    dependencies=[Depends(AdminPermission())],
)
async def create_announcement(
    data: AnnouncementCreate,
    slug: str = Path(..., description="Slug of the cafe"),
    current_user: User = Depends(get_current_user),
):
    """Create an announcement. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    return await AnnouncementService.create(current_user, cafe, data)


@announcement_router.put(
    "/cafes/{slug}/announcements/{id}",
    response_model=AnnouncementOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    dependencies=[Depends(AdminPermission())],
)
async def update_announcement(
    data: AnnouncementUpdate,
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the announcement"),
):
    """Update an announcement. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    announcement = await AnnouncementService.get_by_id_and_cafe_id(id, cafe.id)
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An announcement with this ID does not exist."}],
        )

    return await AnnouncementService.update(announcement, data)


@announcement_router.delete(
    "/cafes/{slug}/announcements/{id}",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    dependencies=[Depends(AdminPermission())],
)
async def delete_announcement(
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the announcement"),
):
    """Delete an announcement. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    announcement = await AnnouncementService.get_by_id_and_cafe_id(id, cafe.id)
    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An announcement with this ID does not exist."}],
        )

    await AnnouncementService.delete(announcement)
