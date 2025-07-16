"""
Module for handling interaction-related enumerations.
"""

from enum import Enum

class TargetType(str, Enum):
    ITEM = "ITEM"
    EVENT = "EVENT"
    POST = "POST"
    DIET = "DIET"
    CAFE = "CAFE"
    COMMENT = "COMMENT"
    ANNOUNCEMENT = "ANNOUNCEMENT"


class InteractionType(str, Enum):
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"
    ATTEND = "ATTEND"
    SUPPORT = "SUPPORT"
    REPORT = "REPORT"
