from typing import List, Optional

from beanie import DecimalAnnotation, PydanticObjectId
from pydantic import BaseModel, Field, field_validator

from app.models.menu_model import MenuItemOption

"""
This module defines the Pydantic-based schemas for menu item operations in the Café application. 
These schemas are utilized for request and response validation, serialization, 
and documentation specific to menu item creation, updates, and retrieval.

Note: These models are for API data interchange related to menu items and not direct database models.
"""


class MenuItemCreate(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=50, description="Name of the menu item."
    )
    tags: List[str] = Field(
        ..., max_length=20, description="List of tags for the menu item."
    )
    description: str = Field(
        ..., min_length=1, max_length=255, description="Description of the menu item."
    )
    image_url: Optional[str] = Field(
        None, max_length=755, description="Image URL of the menu item."
    )
    price: DecimalAnnotation = Field(..., description="Price of the menu item.")
    in_stock: bool = Field(..., description="Availability status of the menu item.")
    category: str = Field(
        ..., min_length=1, max_length=50, description="Category of the menu item."
    )
    options: List[MenuItemOption] = Field(
        ..., description="Options available for the menu item."
    )

    @field_validator("price")
    @classmethod
    def validate_price(cls, price):
        if price < 0:
            raise ValueError("Price must be a non-negative value.")
        return price


class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=50, description="Updated name of the menu item."
    )
    tags: Optional[List[str]] = Field(
        None, max_length=20, description="Updated tags for the menu item."
    )
    description: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Updated description of the menu item.",
    )
    image_url: Optional[str] = Field(
        None, max_length=755, description="Updated image URL of the menu item."
    )
    price: Optional[DecimalAnnotation] = Field(
        None, description="Updated price of the menu item."
    )
    in_stock: Optional[bool] = Field(
        None, description="Updated availability status of the menu item."
    )
    category: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="Updated category of the menu item.",
    )
    options: Optional[List[MenuItemOption]] = Field(
        None, description="Updated options for the menu item."
    )

    @field_validator("price")
    @classmethod
    def validate_price(cls, price):
        if price < 0:
            raise ValueError("Price must be a non-negative value.")
        return price


class MenuItemOut(BaseModel):
    id: PydanticObjectId = Field(..., description="Unique identifier of the menu item.")
    cafe_id: PydanticObjectId = Field(
        ..., description="ID of the cafe this menu item belongs to."
    )
    name: str = Field(..., description="Name of the menu item.")
    tags: List[str] = Field(..., description="Tags associated with the menu item.")
    description: str = Field(..., description="Description of the menu item.")
    image_url: Optional[str] = Field(None, description="Image URL of the menu item.")
    price: DecimalAnnotation = Field(..., description="Price of the menu item.")
    in_stock: bool = Field(..., description="Availability status of the menu item.")
    category: str = Field(..., description="Category of the menu item.")
    options: List[MenuItemOption] = Field(
        ..., description="Options available for the menu item."
    )
