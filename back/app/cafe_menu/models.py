"""
Module for handling menu-related models.
"""

from typing import List, Optional

import pymongo
from beanie import DecimalAnnotation, Document
from pydantic import BaseModel, Field, field_validator
from pymongo import IndexModel

from app.models import CafeId, CategoryId, Id, IdAlias, IdDefaultFactory


class MenuItemOption(BaseModel):
    """Model for menu item options."""

    type: str = Field(..., min_length=1)
    value: str = Field(..., min_length=1)
    fee: DecimalAnnotation

    @field_validator("fee")
    @classmethod
    def validate_fee(cls, fee):
        """Validate fee value."""
        if fee < DecimalAnnotation(0.0):
            raise ValueError("Fee must be a non-negative value.")
        return fee


class MenuItemBase(BaseModel):
    """Base model for menu items."""

    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    tags: Optional[List[str]] = Field(None, max_length=20)
    image_url: Optional[str] = Field(None, max_length=755)
    price: DecimalAnnotation
    in_stock: bool
    options: List[MenuItemOption]

    @field_validator("price")
    @classmethod
    def validate_price(cls, price):
        """Validate price value."""
        if price < DecimalAnnotation(0.0):
            raise ValueError("Price must be a non-negative value.")
        return price


class MenuItem(Document, MenuItemBase, CategoryId, CafeId):
    """Menu item document model."""

    class Settings:
        """Settings for menu item document."""

        name = "menus"
        indexes = [
            IndexModel([("cafe_id", pymongo.ASCENDING)]),
            IndexModel([("category_id", pymongo.ASCENDING)]),
            IndexModel([("name", pymongo.ASCENDING)]),
            IndexModel([("description", pymongo.ASCENDING)]),
        ]


class MenuItemCreate(MenuItemBase, CategoryId):
    """Model for creating menu items."""

    pass


class MenuItemUpdate(BaseModel, CategoryId):
    """Model for updating menu items."""

    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    tags: Optional[List[str]] = Field(None, max_length=20)
    image_url: Optional[str] = Field(None, max_length=755)
    price: Optional[DecimalAnnotation] = None
    in_stock: Optional[bool] = None
    options: Optional[List[MenuItemOption]] = None

    @field_validator("price")
    @classmethod
    def validate_price(cls, price):
        """Validate price value."""
        if price < DecimalAnnotation(0.0):
            raise ValueError("Price must be a non-negative value.")
        return price


class MenuItemOut(MenuItemBase, CategoryId, CafeId, Id):
    """Model for menu item output."""

    pass


class MenuItemView(MenuItemBase, IdAlias):
    """Model for menu item views."""

    pass


class MenuItemViewOut(MenuItemBase, Id):
    """Model for menu item view output."""

    pass


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


class MenuBase(BaseModel):
    """Base model for menus."""

    category: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, min_length=1, max_length=255)


class MenuView(MenuBase, IdAlias):
    """Model for menu view."""

    items: List[MenuItemView]


class MenuViewOut(MenuBase, Id):
    """Model for menu view output."""

    items: List[MenuItemViewOut]
