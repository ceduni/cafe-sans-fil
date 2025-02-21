from datetime import datetime
from typing import List, Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class UserInteraction(BaseModel):
    user_id: PydanticObjectId
    interaction_time: datetime = Field(default_factory=datetime.now)


class Announcement(Document):
    cafe_id: PydanticObjectId
    title: str = Field(..., min_length=1)
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    active_until: Optional[datetime] = None
    likes: List[UserInteraction] = []
    tags: List[str] = []

    class Settings:
        name = "announcements"


class AnnouncementCreate(BaseModel):
    cafe_id: PydanticObjectId
    title: str = Field(..., min_length=1)
    content: str
    active_until: Optional[datetime] = None
    tags: List[str] = []


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    active_until: Optional[datetime] = None
    tags: Optional[List[str]] = None


class AnnouncementOut(BaseModel):
    id: PydanticObjectId
    cafe_id: PydanticObjectId
    title: str = Field(..., min_length=1)
    content: str
    created_at: datetime
    active_until: Optional[datetime] = None
    likes: List[UserInteraction] = []
    tags: List[str] = []
