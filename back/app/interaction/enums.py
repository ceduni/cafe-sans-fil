"""
Module for handling interaction-related enumerations.
"""

from enum import Enum


class InteractionType(str, Enum):
    """Interaction types."""

    # Base interactions
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"

    # Event interactions
    ATTEND = "ATTEND"
    SUPPORT = "SUPPORT"
