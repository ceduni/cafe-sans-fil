from datetime import datetime
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
from pydantic import BaseModel, Field, field_validator
from pymongo import IndexModel

from app.models import CafeId, Id, ItemId, UserId
from app.order.enums import OrderStatus


class OrderedItemOption(BaseModel):
    type: str
    value: str
    fee: DecimalAnnotation

    @field_validator("fee")
    @classmethod
    def validate_fee(cls, fee):
        if fee < DecimalAnnotation(0.0):
            raise ValueError("Fee must be a non-negative value.")
        return fee


class OrderedItem(BaseModel, ItemId):
    item_name: str
    item_image_url: Optional[str] = None
    item_price: DecimalAnnotation
    quantity: int
    options: List[OrderedItemOption]

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        return quantity


class OrderBase(BaseModel):
    order_number: int
    cafe_name: str
    cafe_image_url: Optional[str] = None
    items: List[OrderedItem]
    total_price: DecimalAnnotation = DecimalAnnotation(0.0)
    status: OrderStatus = Field(default=OrderStatus.PLACED)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class Order(Document, OrderBase, CafeId, UserId):
    @before_event([Replace, Insert])
    def calculate_total_price(self):
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
        self.updated_at = datetime.utcnow()

    class Settings:
        name = "orders"
        indexes = [
            IndexModel([("order_number", pymongo.ASCENDING)], unique=True),
        ]


class OrderCreate(BaseModel):
    cafe_id: PydanticObjectId
    cafe_name: str
    cafe_image_url: Optional[str] = None
    items: List[OrderedItem]

    @field_validator("items")
    @classmethod
    def validate_items(cls, v):
        if not v:
            raise ValueError("Order must include at least one item.")
        return v


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None


class OrderOut(OrderBase, CafeId, UserId, Id):
    pass
