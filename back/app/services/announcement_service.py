from typing import List
from app.models.announcement_model import Announcement, UserInteraction
from app.schemas.announcement_schema import AnnouncementCreate, AnnouncementOut
from uuid import UUID

class AnnouncementService:
    async def get_announcements(**query_params) -> List[AnnouncementOut]:
        sort_by = query_params.pop("sort_by", "start_date")
        page = int(query_params.pop("page", 1))
        limit = int(query_params.pop("limit", 9))
        return (
            await Announcement.find(query_params)
            .skip((page - 1) * limit)
            .limit(limit)
            .sort(sort_by)
            .to_list()
        )

    async def create_announcement(announcement_data: AnnouncementCreate) -> AnnouncementOut:
        announcement = Announcement(**announcement_data.model_dump())
        await announcement.insert()
        return announcement

    async def update_announcement(announcement_id: UUID, announcement_data: AnnouncementCreate) -> AnnouncementOut:
        announcement = await Announcement.find_one(Announcement.announcement_id == announcement_id)
        if not announcement:
            raise ValueError("Announcement not found")
        for key, value in announcement_data.dict(exclude_unset=True).items():
            setattr(announcement, key, value)
        await announcement.save()
        return announcement
    
    async def remove_announcement(announcement_id: UUID) -> AnnouncementOut:
        announcement = await Announcement.find_one(Announcement.announcement_id == announcement_id)
        if not announcement:
            raise ValueError("Announcement not found")
        await announcement.delete()
        return announcement
    
    async def add_like_to_announcement(announcement_id: UUID, user_id: UUID) -> AnnouncementOut:
        announcement = await Announcement.find_one(Announcement.announcement_id == announcement_id)
        if not announcement:
            raise ValueError("Announcement not found")
        if not any(li.user_id == user_id for li in announcement.likes):
            announcement.likes.append(UserInteraction(user_id=user_id))
            await announcement.save()
        return announcement

    async def remove_like_from_announcement(announcement_id: UUID, user_id: UUID) -> AnnouncementOut:
        announcement = await Announcement.find_one(Announcement.announcement_id == announcement_id)
        if not announcement:
            raise ValueError("Announcement not found")
        original_likes = len(announcement.likes)
        announcement.likes = [like for like in announcement.likes if like.user_id != user_id]
        if len(announcement.likes) < original_likes:
            await announcement.save()
        return announcement
