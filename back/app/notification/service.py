"""
Module for handling interaction-related operations.
"""

from typing import Any, Dict, List, Union

from beanie import PydanticObjectId
from beanie.odm.queries.find import AggregationQuery

from app.notification.models import (
    Notification,
    NotificationType,
)
from app.user.models import User


class NotificationService:
    """Service for handling interaction-related operations."""

    @staticmethod
    async def get_all(to_list: bool = True,**filters: dict) -> Union[AggregationQuery[List[Dict[str, Any]]], List[Dict[str, Any]]]:
        """Get user notifications."""
        
        return await query.to_list() if to_list else query


    @staticmethod
    async def create(user: User, type: NotificationType) -> None:
        """Create an interaction."""
        # TODO: Implement the logic to create a notification.


    @staticmethod
    async def update(user: User, read:bool) -> None:
        """Create an interaction."""
        # TODO: Implement the logic to update a notification.


    @staticmethod
    async def delete(notification: Notification) -> None:
        """Delete an interaction."""
        # TODO: Implement the logic to delete a notification.

  