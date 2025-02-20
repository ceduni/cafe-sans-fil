from datetime import datetime
from typing import List, Optional

from beanie import DecimalAnnotation, PydanticObjectId
from pydantic import BaseModel, Field, field_validator

from app.order.models import OrderedItem, OrderStatus

"""
This module defines the Pydantic-based schemas for order operations in the Café application. 
These schemas are utilized for request and response validation, serialization, 
and documentation specific to orders.

Note: These models are for API data interchange related to orders and not direct database models.
"""

# --------------------------------------
#               Order
# --------------------------------------


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


class OrderOut(BaseModel):
    id: PydanticObjectId
    order_number: int
    user_id: PydanticObjectId
    cafe_id: PydanticObjectId
    cafe_name: str
    cafe_image_url: Optional[str] = None
    items: List[OrderedItem]
    total_price: DecimalAnnotation
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
