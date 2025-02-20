from typing import List, Optional

from beanie import DecimalAnnotation, Document, Indexed, PydanticObjectId
from pydantic import BaseModel, Field, field_validator


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


class MenuItemEmbedded(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    name: str
    description: str
    image_url: Optional[str] = None
    price: DecimalAnnotation
    in_stock: bool = False
    category: str
    options: List[MenuItemOption]


class MenuItem(Document):
    cafe_id: PydanticObjectId
    name: Indexed(str)
    tags: List[str]
    description: Indexed(str)
    image_url: Optional[str] = None
    price: DecimalAnnotation
    in_stock: bool = False
    category: Indexed(str)
    options: List[MenuItemOption]

    @field_validator("price")
    @classmethod
    def validate_price(cls, price):
        if price < DecimalAnnotation(0.0):
            raise ValueError("Price must be a non-negative value.")
        return price

    class Settings:
        name = "menus"
