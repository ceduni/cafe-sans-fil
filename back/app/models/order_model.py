from typing import List
from uuid import UUID, uuid4
from beanie import Document, DecimalAnnotation, before_event, Replace, Insert
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

class OrderedItemOption(BaseModel):
    type: str = Field(..., description="Type of the option.")
    value: str = Field(..., description="Value of the option.")
    fee: DecimalAnnotation = Field(..., description="Additional fee for this option.")

class OrderedItem(BaseModel):
    item_id: UUID = Field(..., description="Unique identifier for the item.")
    quantity: int = Field(..., description="Quantity of the item ordered.")
    item_price: DecimalAnnotation = Field(..., description="Price per unit of the item.")
    options: List[OrderedItemOption] = Field(..., description="List of options selected for this item.")

class OrderStatus(str, Enum):
    PLACED = "Placée"
    READY = "Prête"
    COMPLETED = "Complétée"
    CANCELLED = "Annulée"

class Order(Document):
    order_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    cafe_id: UUID
    items: List[OrderedItem]
    total_price: DecimalAnnotation = DecimalAnnotation(0.0)
    status: OrderStatus = Field(default=OrderStatus.PLACED)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @before_event([Replace, Insert])
    def calculate_total_price(self):
        total = sum(
            DecimalAnnotation(item.quantity) * (item.item_price + sum(DecimalAnnotation(option.fee) for option in item.options))
            for item in self.items
        )
        self.total_price = total.quantize(DecimalAnnotation('0.00'))

    @before_event([Replace, Insert])
    def update_update_at(self):
        self.updated_at = datetime.utcnow()
        
    class Settings:
        name = "orders"


