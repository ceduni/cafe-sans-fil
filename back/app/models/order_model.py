from typing import List
from uuid import UUID, uuid4
from beanie import Document, before_event, Replace, Insert
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum
from decimal import Decimal
from bson.decimal128 import Decimal128
"""
This module defines the Pydantic-based models used in the Café application for order management, 
which are specifically designed for database interaction via the Beanie ODM 
(Object Document Mapper) for MongoDB. These models outline the structure, relationships, 
and constraints of the order-related data stored in the database.

Note: These models are intended for direct database interactions related to orders and are 
different from the API data interchange models.
"""

def convert_decimal128(value):
    if isinstance(value, Decimal128):
        return Decimal(value.to_decimal())
    return Decimal(str(value))

class OrderedItemOption(BaseModel):
    type: str
    value: str
    fee: Decimal

    # TODO[pydantic]: We couldn't refactor the `validator`, please replace it by `field_validator` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-validators for more information.
    @validator('fee', pre=True, always=True)
    def format_fee(cls, v):
        return convert_decimal128(v).quantize(Decimal('0.00'))

class OrderedItem(BaseModel):
    item_id: UUID
    quantity: int
    item_price: Decimal
    options: List[OrderedItemOption]

    # TODO[pydantic]: We couldn't refactor the `validator`, please replace it by `field_validator` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-validators for more information.
    @validator('item_price', pre=True, always=True)
    def format_item_price(cls, v):
        return convert_decimal128(v).quantize(Decimal('0.00'))

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
    total_price: Decimal = Decimal(0.0)
    status: OrderStatus = Field(default=OrderStatus.PLACED)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # TODO[pydantic]: We couldn't refactor the `validator`, please replace it by `field_validator` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-validators for more information.
    @validator('total_price', pre=True, always=True)
    def format_total_price(cls, v):
        return convert_decimal128(v).quantize(Decimal('0.00'))
    
    @before_event([Replace, Insert])
    def calculate_total_price(self):
        total = sum(
            Decimal(item.quantity) * (item.item_price + sum(Decimal(option.fee) for option in item.options))
            for item in self.items
        )
        self.total_price = total.quantize(Decimal('0.00'))

    @before_event([Replace, Insert])
    def update_update_at(self):
        self.updated_at = datetime.utcnow()
        
    class Settings:
        name = "orders"


