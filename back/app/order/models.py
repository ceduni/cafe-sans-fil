"""
Module for handling order-related models.
"""

from datetime import UTC, datetime
from typing import List, Optional

import pymongo
from beanie import DecimalAnnotation, Document, Insert, Save, before_event
from pydantic import BaseModel, Field, field_validator
from pymongo import IndexModel

from app.cafe.menu.item.models import MenuItemOption
from app.models import CafeId, Id, IdAlias, ItemId, UserId
from app.order.enums import OrderStatus


class OrderedItem(BaseModel, IdAlias):
    """Model for ordered menu items."""

    name: str
    price: DecimalAnnotation
    quantity: int = Field(default=1)
    options: List[MenuItemOption]

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, quantity):
        """Validate quantity value."""
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        return quantity


class OrderBase(BaseModel):
    """Base model for orders."""

    cafe_name: str
    order_number: int
    items: List[OrderedItem]
    total_price: DecimalAnnotation = DecimalAnnotation(0.0)
    status: OrderStatus = Field(default=OrderStatus.PLACED)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(UTC))


class Order(Document, OrderBase, CafeId, UserId):
    """Order document model."""

    @before_event([Insert, Save])
    def calculate_total_price(self):
        """Calculate total price."""
        total = sum(
            DecimalAnnotation(item.quantity)
            * (
                item.price
                + sum(DecimalAnnotation(option.fee) for option in item.options)
            )
            for item in self.items
        )
        if total < 0:
            raise ValueError("Total price must be a non-negative value.")
        self.total_price = total.quantize(DecimalAnnotation("0.00"))

    @before_event([Insert, Save])
    def update_update_at(self):
        """Update updated_at field."""
        self.updated_at = datetime.now(UTC)

    class Settings:
        """Settings for order document."""

        name = "orders"
        indexes = [
            IndexModel([("user_id", pymongo.ASCENDING)]),
            IndexModel([("cafe_id", pymongo.ASCENDING)]),
            IndexModel([("order_number", pymongo.ASCENDING)]),
            IndexModel([("status", pymongo.ASCENDING)]),
            IndexModel([("created_at", pymongo.ASCENDING)]),
            IndexModel([("updated_at", pymongo.ASCENDING)]),
            IndexModel(
                [("status", pymongo.ASCENDING), ("created_at", pymongo.ASCENDING)]
            ),
        ]


class OrderedItemCreate(BaseModel, ItemId):
    """Model for creating ordered items."""

    quantity: int = Field(default=1)
    options: List[MenuItemOption]

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, quantity):
        """Validate quantity value."""
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        return quantity


class OrderedItemOut(BaseModel, Id):
    """Model for ordered item output."""

    name: str
    price: DecimalAnnotation
    quantity: int = Field(default=1)
    options: List[MenuItemOption]


class OrderCreate(BaseModel):
    """Model for creating orders."""

    items: List[OrderedItemCreate]

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

    items: List[OrderedItemOut]
