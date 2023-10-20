from typing import List, Optional
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

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
    order_timestamp: datetime
    completion_time: Optional[datetime] = None

    class Collection:
        name = "orders"


