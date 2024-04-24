from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID

from app.schemas.announcement_schema import AnnouncementCreate, AnnouncementOut
from app.services.announcement_service import create_announcement, get_announcements

announcement_router = APIRouter()

@announcement_router.get("/announcements/", response_model=List[AnnouncementOut])
async def list_announcements_handler():
    return await get_announcements()

@announcement_router.post("/announcements/", response_model=AnnouncementOut)
async def create_announcement_handler(announcement: AnnouncementCreate):
    return await create_announcement(announcement)

