"""
Module for handling order-related enumerations
"""

from enum import Enum


class OrderStatus(str, Enum):
    """Order status enumeration."""

    PLACED = "Placée"
    READY = "Prête"
    COMPLETED = "Complétée"
    CANCELLED = "Annulée"
