"""
Module for handling menu-related models.
"""

from typing import List

from pydantic import BaseModel

from app.cafe.menu.category.models import MenuCategory, MenuCategoryItemOut
from app.cafe.menu.enums import Layout


class Menu(BaseModel):
    """Model for menu."""

    layout: Layout
    categories: List[MenuCategory] = []


class MenuUpdate(BaseModel):
    """Model for updating menu."""

    layout: Layout


class MenuOut(BaseModel):
    """Model for menu output."""

    layout: Layout
    categories: List[MenuCategoryItemOut] = []
