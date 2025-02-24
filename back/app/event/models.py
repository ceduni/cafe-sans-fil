"""
Module for handling event-related models.
"""

from datetime import UTC, datetime
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field

from app.models import CafeId, Id, UserId


class UserInteraction(BaseModel, UserId):
    """Model for user interactions."""

    interaction_time: datetime = Field(default_factory=lambda: datetime.now(UTC))


class EventBase(BaseModel):
    """Base model for events."""

    title: str = Field(..., min_length=1)
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    image_url: Optional[str] = None
    attendees: List[UserInteraction] = []
    supporters: List[UserInteraction] = []


class Event(Document, EventBase, CafeId):
    """Event document model."""

    class Settings:
        """Settings for event document."""

        name = "events"


class EventCreate(BaseModel, CafeId):
    """Model for creating events."""

    title: str = Field(..., min_length=1)
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    image_url: Optional[str] = None


class EventUpdate(BaseModel):
    """Model for updating events."""

    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    image_url: Optional[str] = None


class EventOut(EventBase, CafeId, Id):
    """Model for event output."""

    pass
