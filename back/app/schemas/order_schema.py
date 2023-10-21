from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

"""
This module defines the Pydantic-based schemas for order operations in the Café application. 
These schemas are utilized for request and response validation, serialization, 
and documentation specific to orders.

Note: These models are for API data interchange related to orders and not direct database models.
"""

class OrderedItem(BaseModel):
    item_id: UUID
    quantity: int
    item_price: float

class OrderStatus(str, Enum):
    PLACED = "placed"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Order(BaseModel):
    user_id: UUID
    cafe_id: UUID
    items: List[OrderedItem]
    total_price: float
    status: OrderStatus
    order_timestamp: datetime
    completion_time: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "cafe_id": "123e4567-e89b-12d3-a456-426614174001",
                "items": [
                    {
                        "item_id": "123e4567-e89b-12d3-a456-426614174002",
                        "quantity": 2,
                        "item_price": 5.0,
                    }
                ],
                "total_price": 10.0,
                "status": "placed",
                "order_timestamp": "2023-10-19T14:30:00",
            }
        }
