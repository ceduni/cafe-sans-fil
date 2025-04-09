"""
Module for handling event-related models.
"""

from datetime import datetime
from typing import List, Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, HttpUrl

from app.interaction.models import InteractionOut
from app.models import Id
from app.user.models import UserOut


class Ticketing(BaseModel):
    ticket_url: HttpUrl
    ticket_price: float

class EventBase(BaseModel):
    """Base model for events."""

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    start_date: datetime
    end_date: datetime
    location: Optional[str] = None
    ticket: Optional[Ticketing] = None


class Event(Document, EventBase):
    """Event document model."""

    cafe_ids: List[PydanticObjectId] = []
    creator_id: PydanticObjectId
    editor_ids: List[PydanticObjectId] = []

    class Settings:
        """Settings for event document."""

        name = "events"


class EventCreate(EventBase):
    """Model for creating events."""

    cafe_ids: Optional[List[PydanticObjectId]] = None
    editor_ids: Optional[List[PydanticObjectId]] = None
    max_support: Optional[int] = None


class EventUpdate(BaseModel):
    """Model for updating events."""

    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    ticket: Optional[Ticketing] = None
    editor_ids: Optional[List[PydanticObjectId]] = None


class EventOut(EventBase, Id):
    """Model for event output."""

    cafe_ids: List[PydanticObjectId]
    creator_id: PydanticObjectId
    editor_ids: List[PydanticObjectId]


class EventCafesOut(BaseModel, Id):
    """Model for event cafes output."""

    name: str = Field(..., min_length=1, max_length=50)
    slug: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    banner_url: Optional[HttpUrl] = None


class EventAggregateOut(EventBase, Id):
    """Model for aggregated event output."""

    cafes: List[EventCafesOut]
    creator: UserOut
    interactions: List[InteractionOut]
    #editors: List[UserOut]
