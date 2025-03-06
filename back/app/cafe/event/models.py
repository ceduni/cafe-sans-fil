"""
Module for handling event-related models.
"""

from datetime import datetime
from typing import List, Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, HttpUrl

from app.interaction.models import InteractionOut
from app.models import CafeId, Id
from app.user.models import UserOut


class EventBase(BaseModel):
    """Base model for events."""

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    start_date: datetime
    end_date: datetime
    location: Optional[str] = None


class Event(Document, EventBase, CafeId):
    """Event document model."""

    creator_id: PydanticObjectId

    class Settings:
        """Settings for event document."""

        name = "events"


class EventCreate(EventBase):
    """Model for creating events."""

    pass


class EventUpdate(BaseModel):
    """Model for updating events."""

    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None


class EventOut(EventBase, CafeId, Id):
    """Model for event output."""

    creator_id: PydanticObjectId


class EventAggregateOut(EventBase, CafeId, Id):
    """Model for aggregated event output."""

    creator: UserOut
    interactions: List[InteractionOut]
