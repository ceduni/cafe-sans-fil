"""
Module for handling announcement-related models.
"""

from datetime import UTC, datetime
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field

from app.models import CafeId, Id, UserId


class UserInteraction(BaseModel, UserId):
    """Model for user interactions."""

    interaction_time: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AnnouncementBase(BaseModel):
    """Base model for announcements."""

    title: str = Field(..., min_length=1)
    content: str
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(UTC))
    active_until: Optional[datetime] = None
    likes: List[UserInteraction] = []
    tags: List[str] = []


class Announcement(Document, AnnouncementBase, CafeId):
    """Announcement document model."""

    class Settings:
        """Document settings."""

        name = "announcements"


class AnnouncementCreate(BaseModel, CafeId):
    """Model for creating announcements."""

    title: str = Field(..., min_length=1)
    content: str
    active_until: Optional[datetime] = None
    tags: List[str] = []


class AnnouncementUpdate(BaseModel):
    """Model for updating announcements."""

    title: Optional[str] = None
    content: Optional[str] = None
    active_until: Optional[datetime] = None
    tags: Optional[List[str]] = None


class AnnouncementOut(AnnouncementBase, CafeId, Id):
    """Model for announcement output."""

    pass
