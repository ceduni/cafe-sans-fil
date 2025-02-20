from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from app.announcement.models import UserInteraction


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
