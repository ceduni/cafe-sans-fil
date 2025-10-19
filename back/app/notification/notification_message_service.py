"""
Module for handling interaction-related operations.
"""

from typing import Any, Dict, List, Union, Optional
from beanie import PydanticObjectId

from app.notification.models import (
    NotificationMessage,
    NotificationType,
)
from app.user.models import User


class NotificationMessageService:
    
    @staticmethod
    async def get_all(to_list: bool = True,**filters: dict) -> Union[List[NotificationMessage], Any]:
        """Get notification messages."""
      
        query = NotificationMessage.find(filters)
        
        return await query.to_list() if to_list else query
    

    @staticmethod
    async def create(data: Dict[str, Any]) -> NotificationMessage:
        """Create a new notification message."""
        msg = NotificationMessage(**data)
        return await msg.insert()

    @staticmethod
    async def get_by_id(msg_id: str) -> Optional[NotificationMessage]:
        """Retrieve a notification message by its ID."""
        try:
            return await NotificationMessage.get(PydanticObjectId(msg_id))
        except Exception:
            return None

    @staticmethod
    async def update(msg_id: str, data: Dict[str, Any]) -> Optional[NotificationMessage]:
        """Update a notification message by ID."""
        msg = await NotificationMessageService.get_by_id(msg_id)
        if not msg:
            return None
        
        for k, v in data.items():
            setattr(msg, k, v)
        
        return await msg.save()

    @staticmethod
    async def delete(msg_id: str) -> bool:
        """Delete a notification message."""
        msg = await NotificationMessageService.get_by_id(msg_id)
        if not msg:
            return False
        await msg.delete()
        return True
