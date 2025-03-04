"""
Module for handling cafe-related enumerations.
"""

from enum import Enum


class Feature(str, Enum):
    """Enum for cafe features."""

    ORDER = "ORDER"
    DISCORD_BOT = "DISCORD_BOT"


class Days(str, Enum):
    """Enum for days of the week."""

    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class PaymentMethod(str, Enum):
    """Enum for payment methods."""

    CASH = "CASH"
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
