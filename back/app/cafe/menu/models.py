"""
Module for handling menu-related models.
"""

from typing import List

from pydantic import BaseModel

from app.cafe.menu.category.models import MenuCategory, MenuCategoryItemOut


class Menu(BaseModel):
    """Model for menu."""

    categories: List[MenuCategory] = []


class MenuOut(BaseModel):
    """Model for menu output."""

    categories: List[MenuCategoryItemOut] = []
