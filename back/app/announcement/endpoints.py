"""
Module for handling announcement-related routes.
"""

from typing import Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Path, Query, Request
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

from app.announcement.models import (
    AnnouncementCreate,
    AnnouncementOut,
    AnnouncementUpdate,
)
from app.announcement.service import AnnouncementService
from app.auth.dependencies import get_current_user
from app.service import parse_query_params
from app.user.models import User

announcement_router = APIRouter()


@announcement_router.get("/announcements/", response_model=Page[AnnouncementOut])
async def get_announcements(
    request: Request,
    cafe_id: Optional[PydanticObjectId] = Query(None, description="Filter by cafe ID"),
    sort_by: Optional[str] = Query(None, description="Sort by a specific field"),
):
    """Get a list of announcements."""
    filters = parse_query_params(dict(request.query_params))
    announcements = await AnnouncementService.get_announcements(**filters)
    return await paginate(announcements)


@announcement_router.post("/announcements/", response_model=AnnouncementOut)
async def create_announcement(announcement: AnnouncementCreate) -> AnnouncementOut:
    """Create an announcement."""
    return await AnnouncementService.create_announcement(announcement)


@announcement_router.put(
    "/announcements/{announcement_id}", response_model=AnnouncementOut
)
async def update_announcement(
    announcement_id: PydanticObjectId, announcement: AnnouncementUpdate
) -> AnnouncementOut:
    """Update an announcement."""
    return await AnnouncementService.update_announcement(announcement_id, announcement)


@announcement_router.delete("/announcements/{announcement_id}")
async def delete_announcement(announcement_id: PydanticObjectId) -> None:
    """Delete an announcement."""
    return await AnnouncementService.remove_announcement(announcement_id)


@announcement_router.post(
    "/announcements/{announcement_id}/like", response_model=AnnouncementOut
)
async def toggle_like(
    announcement_id: PydanticObjectId = Path(..., description="Announcement ID"),
    current_user: User = Depends(get_current_user),
    unlike: bool = False,
) -> AnnouncementOut:
    """Toggle like on an announcement."""
    if not unlike:
        return await AnnouncementService.add_like_to_announcement(
            announcement_id, current_user.id
        )
    else:
        return await AnnouncementService.remove_like_from_announcement(
            announcement_id, current_user.id
        )
