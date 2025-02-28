"""
Module for handling order-related models.
"""

from datetime import UTC, datetime
from typing import List, Optional

import pymongo
from beanie import (
    DecimalAnnotation,
    Document,
    Insert,
    PydanticObjectId,
    Replace,
    before_event,
)
from pydantic import BaseModel, Field, HttpUrl, field_validator
from pymongo import IndexModel

from app.models import CafeId, Id, ItemId, UserId
from app.order.enums import OrderStatus


class OrderedItemOption(BaseModel):
    """Model for ordered item options."""

    type: str
    value: str
    fee: DecimalAnnotation

    @field_validator("fee")
    @classmethod
    def validate_fee(cls, fee):
        """Validate fee value."""
        if fee < DecimalAnnotation(0.0):
            raise ValueError("Fee must be a non-negative value.")
        return fee


class OrderedItem(BaseModel, ItemId):
    """Model for ordered items."""

    item_name: str
    item_image_url: Optional[HttpUrl] = None
    item_price: DecimalAnnotation
    quantity: int
    options: List[OrderedItemOption]

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, quantity):
        """Validate quantity value."""
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        return quantity


class OrderBase(BaseModel):
    """Base model for orders."""

    order_number: int
    cafe_name: str
    cafe_image_url: Optional[HttpUrl] = None
    items: List[OrderedItem]
    total_price: DecimalAnnotation = DecimalAnnotation(0.0)
    status: OrderStatus = Field(default=OrderStatus.PLACED)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(UTC))


class Order(Document, OrderBase, CafeId, UserId):
    """Order document model."""

    @before_event([Replace, Insert])
    def calculate_total_price(self):
        """Calculate total price."""
        total = sum(
            DecimalAnnotation(item.quantity)
            * (
                item.item_price
                + sum(DecimalAnnotation(option.fee) for option in item.options)
            )
            for item in self.items
        )
        if total < 0:
            raise ValueError("Total price must be a non-negative value.")
        self.total_price = total.quantize(DecimalAnnotation("0.00"))

    # Comment this function if using generate_data.py to allow randomized updated_at
    @before_event([Replace, Insert])
    def update_update_at(self):
        """Update updated_at field."""
        self.updated_at = datetime.now(UTC)

    class Settings:
        """Settings for order document."""

        name = "orders"
        indexes = [
            IndexModel([("order_number", pymongo.ASCENDING)], unique=True),
        ]


class OrderCreate(BaseModel):
    """Model for creating orders."""

    cafe_id: PydanticObjectId
    cafe_name: str
    cafe_image_url: Optional[HttpUrl] = None
    items: List[OrderedItem]

    @field_validator("items")
    @classmethod
    def validate_items(cls, v):
        """Validate items field."""
        if not v:
            raise ValueError("Order must include at least one item.")
        return v


class OrderUpdate(BaseModel):
    """Model for updating orders."""

    status: Optional[OrderStatus] = None


class OrderOut(OrderBase, CafeId, UserId, Id):
    """Model for order output."""

    pass
