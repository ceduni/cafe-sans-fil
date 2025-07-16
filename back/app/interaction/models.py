"""
Module for handling interaction-related models.
"""

from datetime import UTC, datetime
from typing import Literal, Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from pymongo import IndexModel

from app.interaction.enums import InteractionType, TargetType


class Interaction(Document):
    """Model for interactions."""

    user_id: PydanticObjectId
    target_id: PydanticObjectId
    target_type: TargetType
    type: InteractionType
    rating: Optional[int] = Field(None, ge=1, le=5)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        """Settings for interaction document."""

        name = "interactions"
        is_root = True
        indexes = [
            IndexModel([("item_id", 1)]),
            IndexModel([("announcement_id", 1)]),
            IndexModel([("event_id", 1)]),
            IndexModel([("user_id", 1), ("item_id", 1), ("type", 1)]),
            IndexModel([("user_id", 1), ("announcement_id", 1), ("type", 1)]),
            IndexModel([("user_id", 1), ("event_id", 1), ("type", 1)]),
        ]


class InteractionOut(BaseModel):
    """Model for interaction output."""

    type: InteractionType
    count: int
    me: bool
