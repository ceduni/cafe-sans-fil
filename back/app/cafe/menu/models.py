"""
Module for handling menu-related models.
"""

from typing import List

from pydantic import BaseModel

from app.cafe.menu.category.models import (
    MenuCategory,
    MenuCategoryView,
    MenuCategoryViewOut,
)


class Menu(BaseModel):
    """Model for menu."""

    categories: List[MenuCategory] = []


class MenuView(BaseModel):
    """Model for menu view."""

    categories: List[MenuCategoryView] = []


class MenuViewOut(BaseModel):
    """Model for menu view output."""

    categories: List[MenuCategoryViewOut] = []
