from typing import List, Optional
from beanie import Document, DecimalAnnotation, Indexed, before_event, Replace, Insert, PydanticObjectId
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum

"""
This module defines the Pydantic-based models used in the Café application for order management, 
which are specifically designed for database interaction via the Beanie ODM 
(Object Document Mapper) for MongoDB. These models outline the structure, relationships, 
and constraints of the order-related data stored in the database.
"""

class OrderedItemOption(BaseModel):
    type: str = Field(..., description="Type of the option.")
    value: str = Field(..., description="Value of the option.")
    fee: DecimalAnnotation = Field(..., description="Additional fee for this option.")

    @field_validator('fee')
    @classmethod
    def validate_fee(cls, fee):
        if fee < DecimalAnnotation(0.0):
            raise ValueError("Fee must be a non-negative value.")
        return fee
    
class OrderedItem(BaseModel):
    item_id: PydanticObjectId = Field(..., description="ID of the item related to this ordered item.")
    item_name: str = Field(..., description="Name of the item at the time of order.")
    item_image_url: Optional[str] = Field(None, description="Image URL of the item at the time of order.")
    item_price: DecimalAnnotation = Field(..., description="Price per unit of the item at the time of order.")
    quantity: int = Field(..., description="Quantity of the item ordered.")
    options: List[OrderedItemOption] = Field(..., description="List of options selected for this item.")

    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        return quantity
    
class OrderStatus(str, Enum):
    PLACED = "Placée"
    READY = "Prête"
    COMPLETED = "Complétée"
    CANCELLED = "Annulée"

class Order(Document):
    order_number: Indexed(int, unique=True)
    user_id: PydanticObjectId
    cafe_id: PydanticObjectId
    cafe_name: str
    cafe_image_url: Optional[str] = None
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
        if total < 0:
            raise ValueError("Total price must be a non-negative value.")
        self.total_price = total.quantize(DecimalAnnotation('0.00'))

    # Comment this function if using generate_data.py to allow randomized updated_at
    @before_event([Replace, Insert])
    def update_update_at(self):
        self.updated_at = datetime.utcnow()
        
    class Settings:
        name = "orders"
