"""
Module for handling interaction-related operations.
"""

from typing import Any, Dict, List, Union, Optional
from beanie import PydanticObjectId

from app.notification.models import (
    NotificationStatus,
    NotificationType,
    UserNotification
)

class UserNotificationService:
    """Service for handling interaction-related operations."""


    @staticmethod
    async def get_all(user_id:str, to_list: bool = True,**filters: dict) -> Union[List[UserNotification], Any]:
        """Get user notifications."""
        
        try:
            filters["user_id"] = PydanticObjectId(user_id)
        except Exception as e:
            raise ValueError(f"Invalid user_id: {user_id}") from e
    
        query = NotificationStatus.find(filters)
        
        return await query.to_list() if to_list else query
    
    
    @staticmethod
    async def get_by_id(user_id:str, message_id: str) -> Optional[UserNotification]:
        """Retrieve a notification by its ID."""
        try:
            filters: dict
            filters["user_id"] = PydanticObjectId(user_id)
            filters["message_id"] = PydanticObjectId(user_id)
            
            return await NotificationStatus.find(filters)
        except Exception:
            return None


    async def count_unread(self, user_id: str) -> int:
            """Count unread notifications for a user."""
            filters: dict
            filters["user_id"] = PydanticObjectId(user_id)
            filters["read"] = False
            
            return await UserNotification.count(filters)