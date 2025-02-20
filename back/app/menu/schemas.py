from typing import List, Optional

from beanie import DecimalAnnotation, PydanticObjectId
from pydantic import BaseModel, Field, field_validator

from app.menu.models import MenuItemOption

"""
This module defines the Pydantic-based schemas for menu item operations in the Café application. 
These schemas are utilized for request and response validation, serialization, 
and documentation specific to menu item creation, updates, and retrieval.

Note: These models are for API data interchange related to menu items and not direct database models.
"""


class MenuItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    tags: List[str] = Field(..., max_length=20)
    description: str = Field(..., min_length=1, max_length=255)
    image_url: Optional[str] = Field(None, max_length=755)
    price: DecimalAnnotation
    in_stock: bool
    category: str = Field(..., min_length=1, max_length=50)
    options: List[MenuItemOption]

    @field_validator("price")
    @classmethod
    def validate_price(cls, price):
        if price < 0:
            raise ValueError("Price must be a non-negative value.")
        return price


class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    tags: Optional[List[str]] = Field(None, max_length=20)
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    image_url: Optional[str] = Field(None, max_length=755)
    price: Optional[DecimalAnnotation] = None
    in_stock: Optional[bool] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    options: Optional[List[MenuItemOption]] = None

    @field_validator("price")
    @classmethod
    def validate_price(cls, price):
        if price < 0:
            raise ValueError("Price must be a non-negative value.")
        return price


class MenuItemOut(BaseModel):
    id: PydanticObjectId
    cafe_id: PydanticObjectId
    name: str
    tags: List[str]
    description: str
    image_url: Optional[str] = None
    price: DecimalAnnotation
    in_stock: bool
    category: str
    options: List[MenuItemOption]
