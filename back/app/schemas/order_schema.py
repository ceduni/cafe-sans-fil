from typing import List, Optional
from uuid import UUID
from pydantic import field_validator, ConfigDict, BaseModel, Field
from datetime import datetime
from beanie import DecimalAnnotation
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
    cafe_id: UUID = Field(..., description="UUID of the cafe associated with the order.")
    cafe_name: str = Field(..., description="Name of the cafe associated with the order.")
    cafe_image_url: Optional[str] = Field(None, description="Image URL of the cafe associated with the order.")
    items: List[OrderedItem] = Field(..., description="List of ordered items including details like item ID, name, quantity, price, and options.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "cafe_id": "123e4567-e89b-12d3-a456-426614174000",
            "cafe_name": "Tore et Fraction",
            "cafe_image_url": "https://example.com/cafe.png",
            "items": [
                {
                    "item_id": "123e4567-e89b-12d3-a456-426614174000",
                    "item_name": "Croissant",
                    "item_price": 2.99,
                    "quantity": 2,
                    "options": [
                        {"type": "taille", "value": "moyenne", "fee": 0.50},
                        {"type": "fromage supplémentaire", "value": "oui", "fee": 1.00}
                    ]
                },
                {
                    "item_id": "223e4567-e89b-12d3-a456-426614174001",
                    "item_name": "Baguette",
                    "item_price": 4.99,
                    "quantity": 1,
                    "options": [
                        {"type": "taille", "value": "grande", "fee": 1.00},
                        {"type": "sauce supplémentaire", "value": "non", "fee": 0.00}
                    ]
                }
            ]
        }
    })

    @field_validator('items')
    @classmethod
    def validate_items(cls, v):
        if not v:
            raise ValueError("Order must include at least one item.")
        return v
    
class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = Field(None, description="Current status of the order, e.g., 'Placée', 'Complétée'.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "status": "Complétée"
        }
    })

class OrderOut(BaseModel):
    id: UUID = Field(..., description="Unique identifier of the order.")
    order_number: int = Field(..., description="Order number of the order.")
    user_id: UUID = Field(..., description="UUID of the user who placed the order.")
    cafe_id: UUID = Field(..., description="UUID of the cafe associated with the order.")
    cafe_name: str = Field(..., description="Name of the cafe associated with the order.")
    cafe_image_url: Optional[str] = Field(None, description="Image URL of the cafe associated with the order.")
    items: List[OrderedItem] = Field(..., description="Detailed list of items included in the order.")
    total_price: DecimalAnnotation = Field(..., description="Total price of the order.")
    status: OrderStatus = Field(..., description="Status of the order, e.g., 'Placée', 'Complétée'.")
    created_at: datetime = Field(..., description="Timestamp when the order was created.")
    updated_at: datetime = Field(..., description="Timestamp when the order was last updated.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "order_number": 1234,
            "user_id": "323e4567-e89b-12d3-a456-426614174001",
            "cafe_id": "423e4567-e89b-12d3-a456-426614174002",
            "cafe_name": "Tore et Fraction",
            "cafe_image_url": "https://example.com/cafe.png",
            "items": [
                {
                    "item_id": "123e4567-e89b-12d3-a456-426614174000",
                    "item_name": "Croissant",
                    "item_price": 2.99,
                    "quantity": 2,
                    "options": [
                        {"type": "taille", "value": "moyenne", "fee": 0.50},
                        {"type": "fromage supplémentaire", "value": "oui", "fee": 1.00}
                    ]
                },
                {
                    "item_id": "223e4567-e89b-12d3-a456-426614174001",
                    "item_name": "Baguette",
                    "item_price": 4.99,
                    "quantity": 1,
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
