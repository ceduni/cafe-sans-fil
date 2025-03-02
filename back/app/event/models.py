"""
Module for handling event-related models.
"""

from datetime import datetime
from typing import Optional

from beanie import Document, PydanticObjectId, View
from pydantic import BaseModel, Field, HttpUrl

from app.models import CafeId, Id, IdAlias
from app.user.models import UserView, UserViewOut


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


class EventView(View, EventBase, CafeId, IdAlias):
    """Model for event view."""

    creator: UserView

    class Settings:
        name = "events_view"
        source = "events"
        pipeline = [
            {
                "$lookup": {
                    "from": "users",
                    "localField": "creator_id",
                    "foreignField": "_id",
                    "pipeline": [
                        {
                            "$project": {
                                "_id": 1,
                                "username": 1,
                                "email": 1,
                                "matricule": 1,
                                "first_name": 1,
                                "last_name": 1,
                                "photo_url": 1,
                            }
                        }
                    ],
                    "as": "creator",
                }
            },
            {"$addFields": {"creator": {"$arrayElemAt": ["$creator", 0]}}},
            {"$unset": "creator_id"},
        ]


class EventViewOut(EventBase, CafeId, Id):
    """Model for event view output."""

    creator: UserViewOut
