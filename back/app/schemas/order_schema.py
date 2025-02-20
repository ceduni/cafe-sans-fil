from datetime import datetime
from typing import List, Optional

from beanie import DecimalAnnotation, PydanticObjectId
from pydantic import BaseModel, Field, field_validator

from app.models.order_model import OrderedItem, OrderStatus

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
    cafe_id: PydanticObjectId = Field(
        ..., description="ID of the cafe associated with the order."
    )
    cafe_name: str = Field(
        ..., description="Name of the cafe associated with the order."
    )
    cafe_image_url: Optional[str] = Field(
        None, description="Image URL of the cafe associated with the order."
    )
    items: List[OrderedItem] = Field(
        ...,
        description="List of ordered items including details like item ID, name, quantity, price, and options.",
    )

    @field_validator("items")
    @classmethod
    def validate_items(cls, v):
        if not v:
            raise ValueError("Order must include at least one item.")
        return v


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = Field(
        None, description="Current status of the order, e.g., 'Placée', 'Complétée'."
    )


class OrderOut(BaseModel):
    id: PydanticObjectId = Field(..., description="Unique identifier of the order.")
    order_number: int = Field(..., description="Order number of the order.")
    user_id: PydanticObjectId = Field(
        ..., description="ID of the user who placed the order."
    )
    cafe_id: PydanticObjectId = Field(
        ..., description="ID of the cafe associated with the order."
    )
    cafe_name: str = Field(
        ..., description="Name of the cafe associated with the order."
    )
    cafe_image_url: Optional[str] = Field(
        None, description="Image URL of the cafe associated with the order."
    )
    items: List[OrderedItem] = Field(
        ..., description="Detailed list of items included in the order."
    )
    total_price: DecimalAnnotation = Field(..., description="Total price of the order.")
    status: OrderStatus = Field(
        ..., description="Status of the order, e.g., 'Placée', 'Complétée'."
    )
    created_at: datetime = Field(
        ..., description="Timestamp when the order was created."
    )
    updated_at: datetime = Field(
        ..., description="Timestamp when the order was last updated."
    )
