from fastapi import APIRouter, HTTPException, Depends, Path
from typing import List
from uuid import UUID

from app.schemas.announcement_schema import AnnouncementCreate, AnnouncementOut
from app.services.announcement_service import AnnouncementService
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user

announcement_router = APIRouter()

@announcement_router.get("/announcements/", response_model=List[AnnouncementOut])
async def list_announcements():
    return await AnnouncementService.get_announcements()

@announcement_router.post("/announcements/", response_model=AnnouncementOut)
async def create_announcement(announcement: AnnouncementCreate):
    return await AnnouncementService.create_announcement(announcement)

@announcement_router.delete("/announcements/{announcement_id}")
async def delete_announcement(announcement_id: UUID):
    return await AnnouncementService.remove_announcement(announcement_id)

@announcement_router.post("/announcements/{announcement_id}/like", response_model=AnnouncementOut)
async def toggle_like(
    announcement_id: UUID = Path(..., description="The ID of the announcement"),
    current_user: User = Depends(get_current_user),
    unlike: bool = False
):
    if not unlike:
        return await AnnouncementService.add_like_to_announcement(announcement_id, current_user.user_id)
    else:
        return await AnnouncementService.remove_like_from_announcement(announcement_id, current_user.user_id)
