"""
Module for handling notification-related enumerations.
"""

from enum import Enum


class NotificationType(str, Enum):
    """Notification types."""

    INFO = "INFO"
    PROMO  = "PROMOTION "
    ALERT = "ALERT"
    UPDATE = "UPDATE"
    EVENT = "EVENT"
    
class ActionType(str, Enum):
    LINK = "link"       # For URL navigation
