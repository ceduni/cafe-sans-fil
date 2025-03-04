"""
Module for handling order-related enumerations
"""

from enum import Enum


class OrderStatus(str, Enum):
    """Order status enumeration."""

    PLACED = "PLACED"  # Placée
    READY = "READY"  # Prête
    COMPLETED = "COMPLETED"  # Complétée
    CANCELLED = "CANCELLED"  # Annulée
