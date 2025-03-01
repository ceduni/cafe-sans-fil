"""
Module for handling announcement-related routes.
"""

from typing import Optional, TypeVar

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Path, Query, Request
from fastapi_pagination import Params
from fastapi_pagination.customization import CustomizedPage, UseParams
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

from app.announcement.models import (
    AnnouncementCreate,
    AnnouncementOut,
    AnnouncementUpdate,
)
from app.announcement.service import AnnouncementService
from app.auth.dependencies import get_current_user
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
    response_model=AnnouncementPage[AnnouncementPage],
)
async def get_announcements(
    request: Request,
):
    """Get a list of announcements."""
    filters = parse_query_params(dict(request.query_params))
    announcements = await AnnouncementService.get_all(**filters)
    return await paginate(announcements)


@announcement_router.post(
    "/announcements/",
    response_model=AnnouncementOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def create_announcement(
    data: AnnouncementCreate,
):
    """Create an announcement."""
    return await AnnouncementService.create(data)


@announcement_router.put(
    "/announcements/{id}",
    response_model=AnnouncementOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def update_announcement(
    data: AnnouncementUpdate,
    id: PydanticObjectId = Path(..., description="ID of the announcement"),
):
    """Update an announcement."""
    announcement = await AnnouncementService.get(id)
    return await AnnouncementService.update(announcement, data)


@announcement_router.delete(
    "/announcements/{id}",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def delete_announcement(
    id: PydanticObjectId = Path(..., description="ID of the announcement"),
):
    """Delete an announcement."""
    announcement = await AnnouncementService.get(id)
    return await AnnouncementService.delete(announcement)


@announcement_router.post(
    "/announcements/{id}/like",
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def toggle_like(
    id: PydanticObjectId = Path(..., description="ID of the announcement"),
    current_user: User = Depends(get_current_user),
    unlike: bool = False,
):
    """Toggle like on an announcement."""
    announcement = await AnnouncementService.get(id)
    if not unlike:
        return await AnnouncementService.add_like(announcement, current_user.id)
    else:
        return await AnnouncementService.remove_like(announcement, current_user.id)
