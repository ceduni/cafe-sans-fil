"""
Module for handling interaction-related models.
"""

from datetime import UTC, datetime
from typing import Literal, Optional

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import IndexModel

from app.interaction.enums import InteractionType


class Interaction(Document):
    """Model for interactions."""

    user_id: PydanticObjectId
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        """Settings for interaction document."""

        name = "interactions"
        is_root = True
        indexes = [
            IndexModel([("user_id", 1), ("item_id", 1), ("type", 1)]),
            IndexModel([("user_id", 1), ("announcement_id", 1), ("type", 1)]),
            IndexModel([("user_id", 1), ("event_id", 1), ("type", 1)]),
        ]


class ItemInteraction(Interaction):
    """Model for item interactions."""

    item_id: PydanticObjectId
    type: Literal[InteractionType.LIKE, InteractionType.DISLIKE]


class AnnouncementInteraction(Interaction):
    """Model for announcement interactions."""

    announcement_id: PydanticObjectId
    type: Literal[InteractionType.LIKE, InteractionType.DISLIKE]


class EventInteraction(Interaction):
    """Model for event interactions."""

    event_id: PydanticObjectId
    type: InteractionType
