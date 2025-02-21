from datetime import datetime
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field

from app.models import CafeId, Id, UserId


class UserInteraction(BaseModel, UserId):
    interaction_time: datetime = Field(default_factory=datetime.now)


class EventBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    image_url: Optional[str] = None
    attendees: List[UserInteraction] = []
    supporters: List[UserInteraction] = []


class Event(Document, EventBase, CafeId):
    class Settings:
        name = "events"


class EventCreate(BaseModel, CafeId):
    title: str = Field(..., min_length=1)
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    image_url: Optional[str] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    image_url: Optional[str] = None


class EventOut(EventBase, CafeId, Id):
    pass
