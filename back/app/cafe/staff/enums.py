"""
Module for handling staff-related enumerations.
"""

from enum import Enum


class Role(str, Enum):
    """Enum for cafe roles."""

    ADMIN = "ADMIN"
    VOLUNTEER = "VOLUNTEER"
