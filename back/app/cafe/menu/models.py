"""
Module for handling menu-related models.
"""

from typing import List

from pydantic import BaseModel, field_validator

from app.cafe.menu.category.models import MenuCategory, MenuCategoryItemOut
from app.cafe.menu.enums import Layout


class Menu(BaseModel):
    """Model for menu."""

    layout: Layout
    categories: List[MenuCategory] = []

    @field_validator("layout", mode="before")
    def capitalize(cls, value):
        """Capitalize value."""
        if isinstance(value, str):
            return value.upper()
        return value


class MenuUpdate(BaseModel):
    """Model for updating menu."""

    layout: Layout

    @field_validator("layout", mode="before")
    def capitalize(cls, value):
        """Capitalize value."""
        if isinstance(value, str):
            return value.upper()
        return value


class MenuOut(BaseModel):
    """Model for menu output."""

    layout: Layout
    categories: List[MenuCategoryItemOut] = []
