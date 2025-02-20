from typing import Dict, List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request

from app.announcement.schemas import (
    AnnouncementCreate,
    AnnouncementOut,
    AnnouncementUpdate,
)
from app.announcement.service import AnnouncementService
from app.auth.dependencies import get_current_user
from app.service import parse_query_params
from app.user.models import User

announcement_router = APIRouter()


@announcement_router.get("/announcements/", response_model=List[AnnouncementOut])
async def list_announcements(
    request: Request,
    cafe_id: Optional[PydanticObjectId] = Query(
        None, description="Filter announcements by cafe ID."
    ),
    sort_by: Optional[str] = Query(
        "-created_at",
        description="Sort announcements by a specific field. Prefix with '-' for descending order (e.g., '-created_at').",
    ),
    page: Optional[int] = Query(
        1, description="Specify the page number for pagination."
    ),
    limit: Optional[int] = Query(
        9, description="Set the number of cafes to return per page."
    ),
):
    query_params = dict(request.query_params)
    parsed_params = parse_query_params(query_params)
    return await AnnouncementService.get_announcements(**parsed_params)


@announcement_router.post("/announcements/", response_model=AnnouncementOut)
async def create_announcement(announcement: AnnouncementCreate):
    return await AnnouncementService.create_announcement(announcement)


@announcement_router.put(
    "/announcements/{announcement_id}", response_model=AnnouncementOut
)
async def update_announcement(
    announcement_id: PydanticObjectId, announcement: AnnouncementUpdate
):
    return await AnnouncementService.update_announcement(announcement_id, announcement)


@announcement_router.delete("/announcements/{announcement_id}")
async def delete_announcement(announcement_id: PydanticObjectId):
    return await AnnouncementService.remove_announcement(announcement_id)


@announcement_router.post(
    "/announcements/{announcement_id}/like", response_model=AnnouncementOut
)
async def toggle_like(
    announcement_id: PydanticObjectId = Path(
        ..., description="The ID of the announcement"
    ),
    current_user: User = Depends(get_current_user),
    unlike: bool = False,
):
    if not unlike:
        return await AnnouncementService.add_like_to_announcement(
            announcement_id, current_user.id
        )
    else:
        return await AnnouncementService.remove_like_from_announcement(
            announcement_id, current_user.id
        )
