"""
Module for handling cafe-related enumerations.
"""

from enum import Enum


class Feature(str, Enum):
    """Enum for cafe features."""

    ORDER = "Order"


class Days(str, Enum):
    """Enum for days of the week."""

    MONDAY = "Lundi"
    TUESDAY = "Mardi"
    WEDNESDAY = "Mercredi"
    THURSDAY = "Jeudi"
    FRIDAY = "Vendredi"
    SATURDAY = "Samedi"
    SUNDAY = "Dimanche"


class Role(str, Enum):
    """Enum for cafe roles."""

    VOLUNTEER = "Bénévole"
    ADMIN = "Admin"
