from typing import List
from app.models.announcement_model import Announcement
from app.schemas.announcement_schema import AnnouncementCreate, AnnouncementOut

async def get_announcements() -> List[AnnouncementOut]:
    return await Announcement.find_all().to_list()

async def create_announcement(announcement_data: AnnouncementCreate) -> AnnouncementOut:
    announcement = Announcement(**announcement_data.model_dump())
    await announcement.insert()
    return announcement