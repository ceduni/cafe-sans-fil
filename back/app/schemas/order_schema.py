from typing import List, Optional
from uuid import UUID
from pydantic import ConfigDict, BaseModel
from datetime import datetime
from decimal import Decimal
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
    user_id: UUID
    cafe_id: UUID
    items: List[OrderedItem]
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "user_id": "123e4567-e89b-12d3-a456-426614174001",
            "cafe_id": "123e4567-e89b-12d3-a456-426614174002",
            "items": [
                {
                    "item_id": "123e4567-e89b-12d3-a456-426614174003",
                    "quantity": 2,
                    "item_price": 2.99,
                    "options": [
                        {"type": "taille", "value": "moyenne", "fee": 0.50},
                        {"type": "fromage supplémentaire", "value": "oui", "fee": 1.00}
                    ]
                },
                {
                    "item_id": "123e4567-e89b-12d3-a456-426614174004",
                    "quantity": 1,
                    "item_price": 4.99,
                    "options": [
                        {"type": "taille", "value": "grande", "fee": 1.00},
                        {"type": "sauce supplémentaire", "value": "non", "fee": 0.00}
                    ]
                }
            ],
        }
    })

class OrderUpdate(BaseModel):
    cafe_id: Optional[UUID] = None
    items: Optional[List[OrderedItem]] = None
    status: Optional[OrderStatus] = None
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "cafe_id": "123e4567-e89b-12d3-a456-426614174002",
            "items": [
                {
                    "item_id": "123e4567-e89b-12d3-a456-426614174003",
                    "quantity": 2,
                    "item_price": 2.99,
                    "options": [
                        {"type": "taille", "value": "moyenne", "fee": 0.50},
                        {"type": "fromage supplémentaire", "value": "oui", "fee": 1.00}
                    ]
                },
                {
                    "item_id": "123e4567-e89b-12d3-a456-426614174004",
                    "quantity": 1,
                    "item_price": 4.99,
                    "options": [
                        {"type": "taille", "value": "grande", "fee": 1.00},
                        {"type": "sauce supplémentaire", "value": "non", "fee": 0.00}
                    ]
                }
            ],
            "status": "Complétée"
        }
    })

class OrderOut(BaseModel):
    order_id: UUID
    user_id: UUID
    cafe_id: UUID
    items: List[OrderedItem]
    total_price: Decimal
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "order_id": "123e4567-e89b-12d3-a456-426614174000",
            "user_id": "123e4567-e89b-12d3-a456-426614174001",
            "cafe_id": "123e4567-e89b-12d3-a456-426614174002",
            "items": [
                {
                    "item_id": "123e4567-e89b-12d3-a456-426614174003",
                    "quantity": 2,
                    "item_price": 2.99,
                    "options": [
                        {"type": "taille", "value": "moyenne", "fee": 0.50},
                        {"type": "fromage supplémentaire", "value": "oui", "fee": 1.00}
                    ]
                },
                {
                    "item_id": "123e4567-e89b-12d3-a456-426614174004",
                    "quantity": 1,
                    "item_price": 4.99,
                    "options": [
                        {"type": "taille", "value": "grande", "fee": 1.00},
                        {"type": "sauce supplémentaire", "value": "non", "fee": 0.00}
                    ]
                }
            ],
            "total_price": 13.47,
            "status": "Complétée",
            "created_at": "2023-10-19T14:30:00",
            "updated_at": "2023-10-19T15:00:00"
        }
    })