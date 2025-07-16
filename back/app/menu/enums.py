"""
Module for handling menu-related enumerations.
"""

from enum import Enum


class Layout(str, Enum):
    """Enum for menu layout."""

    GRID = "GRID"
    LIST = "LIST"
