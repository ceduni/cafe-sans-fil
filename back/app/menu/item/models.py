"""
Module for handling item-related models.
"""

from typing import List, Optional

import pymongo
from beanie import DecimalAnnotation
from pydantic import BaseModel, Field, HttpUrl, field_validator
from pymongo import IndexModel

from app.interaction.models import InteractionOut
from app.models import CafeId, CategoryIds, CustomDocument, Id


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
   
    
class NutritionInfo(BaseModel):
    calories: Optional[DecimalAnnotation] = Field(None, description="Calories in the item.")
    lipids: Optional[DecimalAnnotation] = Field(None, description="Lipid content in the item.")
    proteins: Optional[DecimalAnnotation] = Field(None, description="Protein content in the item.")
    carbohydrates: Optional[DecimalAnnotation] = Field(None, description="Carbohydrate content in the item.")
    sugar: Optional[DecimalAnnotation] = Field(None, description="Sugar content in the item.")
    sodium: Optional[DecimalAnnotation] = Field(None, description="Salt content in the item.")
    fiber: Optional[DecimalAnnotation] = Field(None, description="Fiber content in the item.")
    saturated_fat: Optional[DecimalAnnotation] = Field(None, description="Saturated fat content in the item.")
    # vitamins: Optional[DecimalAnnotation] = Field(None, description="Vitamins content in the item.")
    #percentage_fruit_vegetables_nuts: Optional[DecimalAnnotation] = Field(None, description="Percentage on fruits, vegetables and nuts in the item.")
    zinc: Optional[DecimalAnnotation] = Field(None, description="Zinc content in the item.")
    iron: Optional[DecimalAnnotation] = Field(None, description="Iron content in the item.")
    calcium: Optional[DecimalAnnotation] = Field(None, description="Calcium content in the item.")
    magnesium: Optional[DecimalAnnotation] = Field(None, description="Magnesium content in the item.")
    potassium: Optional[DecimalAnnotation] = Field(None, description="Potassium content in the item.")
    vitamina: Optional[DecimalAnnotation] = Field(None, description="VitaminA content in the item.")
    vitaminc: Optional[DecimalAnnotation] = Field(None, description="vitaminC content in the item.")
    vitamind: Optional[DecimalAnnotation] = Field(None, description="vitaminD content in the item.")
    vitamine: Optional[DecimalAnnotation] = Field(None, description="vitaminE content in the item.")
    vitamink: Optional[DecimalAnnotation] = Field(None, description="vitaminK content in the item.")
    vitaminb6: Optional[DecimalAnnotation] = Field(None, description="vitaminB6 content in the item.")
    vitaminb12: Optional[DecimalAnnotation] = Field(None, description="vitaminB12 content in the item.")


class MenuItemBase(BaseModel):
    """Base model for menu items."""

    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    tags: Optional[List[str]] = Field(None, max_length=20)
    image_url: Optional[HttpUrl] = None
    price: DecimalAnnotation
    in_stock: bool
    is_highlighted: bool = Field(default=False, description="Whether the item is highlighted/featured.")
    likes: List[str] = Field(..., default_factory=list, description="List containing the ids of the users that liked this item.")
    barecode: Optional[str] = Field(default=None, description="Food's barecode.")
    nutritional_informations: NutritionInfo = Field(default_factory=NutritionInfo, description="Dictionnary of the nutritive values of an item.")
    health_score: float = Field(default=0, description="Item health score.")
    options: List[MenuItemOption]

    @field_validator("price")
    @classmethod
    def validate_price(cls, price):
        """Validate price value."""
        if price < DecimalAnnotation(0.0):
            raise ValueError("Price must be a non-negative value.")
        return price


class MenuItem(CustomDocument, MenuItemBase, CategoryIds, CafeId):
    """Menu item document model."""

    class Settings:
        """Settings for menu item document."""

        name = "items"
        indexes = [
            IndexModel([("cafe_id", pymongo.ASCENDING)]),
            IndexModel([("category_ids", pymongo.ASCENDING)]),
            IndexModel([("name", pymongo.ASCENDING)]),
            IndexModel([("description", pymongo.ASCENDING)]),
            IndexModel([("_id", pymongo.ASCENDING), ("cafe_id", pymongo.ASCENDING)]),
            IndexModel(
                [("cafe_id", pymongo.ASCENDING), ("name", pymongo.ASCENDING)],
                unique=True,
            ),
        ]


class MenuItemCreate(MenuItemBase, CategoryIds):
    """Model for creating menu items."""

    pass


class MenuItemUpdate(BaseModel, CategoryIds):
    """Model for updating menu items."""

    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    tags: Optional[List[str]] = Field(None, max_length=20)
    image_url: Optional[HttpUrl] = None
    price: Optional[DecimalAnnotation] = None
    in_stock: Optional[bool] = None
    is_highlighted: Optional[bool] = None
    options: Optional[List[MenuItemOption]] = None

    @field_validator("price")
    @classmethod
    def validate_price(cls, price):
        """Validate price value."""
        if price < DecimalAnnotation(0.0):
            raise ValueError("Price must be a non-negative value.")
        return price


class MenuItemOut(MenuItemBase, CategoryIds, CafeId, Id):
    """Model for menu item output."""

    pass


class MenuItemAggregateOut(MenuItemBase, Id):
    """Model for menu item aggregate output."""

    interactions: List[InteractionOut]
