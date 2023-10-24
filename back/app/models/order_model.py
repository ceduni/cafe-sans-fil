from typing import List, Optional
from uuid import UUID, uuid4
from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

"""
This module defines the Pydantic-based models used in the Café application for order management, 
which are specifically designed for database interaction via the Beanie ODM 
(Object Document Mapper) for MongoDB. These models outline the structure, relationships, 
and constraints of the order-related data stored in the database.

Note: These models are intended for direct database interactions related to orders and are 
different from the API data interchange models.
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

class Order(Document):
    order_id: UUID = Field(default_factory=uuid4, unique=True)
    user_id: UUID
    cafe_id: UUID
    items: List[OrderedItem]
    total_price: float
    status: OrderStatus
    order_timestamp: datetime = Field(default_factory=datetime.utcnow)
    completion_time: Optional[datetime] = None

    class Collection:
        name = "orders"


