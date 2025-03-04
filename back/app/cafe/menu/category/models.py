"""
Module for handling category-related models.
"""

from typing import List, Optional

from pydantic import BaseModel, Field

from app.cafe.menu.item.models import MenuItemNoRefOut
from app.models import Id, IdDefaultFactory, IdOptional


class MenuCategoryBase(BaseModel):
    """Base model for menu categories."""

    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, min_length=1, max_length=255)


class MenuCategory(MenuCategoryBase, IdDefaultFactory):
    """Model for menu categories."""

    pass


class MenuCategoryCreate(MenuCategoryBase):
    """Model for creating menu categories."""

    pass


class MenuCategoryUpdate(BaseModel):
    """Model for updating menu categories."""

    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, min_length=1, max_length=255)


class MenuCategoryOut(MenuCategoryBase, Id):
    """Model for menu category output."""

    pass


class MenuCategoryItemOut(BaseModel, IdOptional):
    """Model for menu category output with items."""

    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    items: List[MenuItemNoRefOut]
