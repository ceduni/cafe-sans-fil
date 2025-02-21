from typing import List, Optional

import pymongo
from beanie import DecimalAnnotation, Document
from pydantic import BaseModel, Field, field_validator
from pymongo import IndexModel

from app.models import CafeId, Id, IdAlias


class MenuItemOption(BaseModel):
    type: str = Field(..., min_length=1)
    value: str = Field(..., min_length=1)
    fee: DecimalAnnotation

    @field_validator("fee")
    @classmethod
    def validate_fee(cls, fee):
        if fee < DecimalAnnotation(0.0):
            raise ValueError("Fee must be a non-negative value.")
        return fee


class MenuItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    tags: Optional[List[str]] = Field(None, max_length=20)
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    image_url: Optional[str] = Field(None, max_length=755)
    price: DecimalAnnotation
    in_stock: bool
    category: str = Field(..., min_length=1, max_length=50)
    options: List[MenuItemOption]

    @field_validator("price")
    @classmethod
    def validate_price(cls, price):
        if price < DecimalAnnotation(0.0):
            raise ValueError("Price must be a non-negative value.")
        return price


class MenuItem(Document, MenuItemBase, CafeId):
    class Settings:
        name = "menus"
        indexes = [
            IndexModel([("name", pymongo.ASCENDING)]),
            IndexModel([("description", pymongo.ASCENDING)]),
            IndexModel([("category", pymongo.ASCENDING)]),
        ]


class MenuItemView(MenuItemBase, IdAlias):
    pass


class MenuItemCreate(MenuItemBase):
    pass


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
        if price < DecimalAnnotation(0.0):
            raise ValueError("Price must be a non-negative value.")
        return price


class MenuItemOut(MenuItemBase, CafeId, Id):
    pass


class MenuItemViewOut(MenuItemBase, Id):
    pass
