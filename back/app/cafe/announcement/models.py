"""
Module for handling announcement-related models.
"""

from datetime import UTC, datetime
from typing import List, Optional

from beanie import Document, PydanticObjectId, View
from pydantic import BaseModel, Field

from app.models import CafeId, Id
from app.user.models import UserOut


class AnnouncementBase(BaseModel):
    """Base model for announcements."""

    title: str = Field(..., min_length=1)
    content: str
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(UTC))
    active_until: Optional[datetime] = None
    tags: List[str] = []


class Announcement(Document, AnnouncementBase, CafeId):
    """Announcement document model."""

    author_id: PydanticObjectId

    class Settings:
        """Document settings."""

        name = "announcements"


class AnnouncementCreate(BaseModel):
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


class AnnouncementView(View, AnnouncementBase, CafeId, Id):
    """Model for announcement view."""

    author: UserOut

    class Settings:
        """Settings for announcement view."""

        name = "announcements_view"
        source = "announcements"
        pipeline = [
            {
                "$lookup": {
                    "from": "users",
                    "localField": "author_id",
                    "foreignField": "_id",
                    "pipeline": [
                        {
                            "$project": {
                                "_id": 0,
                                "id": "$_id",
                                "username": 1,
                                "email": 1,
                                "matricule": 1,
                                "first_name": 1,
                                "last_name": 1,
                                "photo_url": 1,
                            }
                        }
                    ],
                    "as": "author",
                }
            },
            {"$addFields": {"author": {"$arrayElemAt": ["$author", 0]}}},
            {"$addFields": {"id": "$_id"}},
            {"$unset": ["_id", "author_id"]},
        ]
