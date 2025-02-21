from datetime import datetime
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field

from app.models import CafeId, Id, UserId


class UserInteraction(BaseModel, UserId):
    interaction_time: datetime = Field(default_factory=datetime.now)


class AnnouncementBase(BaseModel):
    title: str = Field(..., min_length=1)
    content: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    active_until: Optional[datetime] = None
    likes: List[UserInteraction] = []
    tags: List[str] = []


class Announcement(Document, AnnouncementBase, CafeId):
    class Settings:
        name = "announcements"


class AnnouncementCreate(BaseModel, CafeId):
    title: str = Field(..., min_length=1)
    content: str
    active_until: Optional[datetime] = None
    tags: List[str] = []


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    active_until: Optional[datetime] = None
    tags: Optional[List[str]] = None


class AnnouncementOut(AnnouncementBase, CafeId, Id):
    pass
