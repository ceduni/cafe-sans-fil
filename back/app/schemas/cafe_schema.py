from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

"""
This module defines the Pydantic-based schemas for cafe operations in the Café application. 
These schemas are utilized for request and response validation, serialization, 
and documentation specific to cafe listings, details, and management.

Note: These models are for API data interchange related to cafes and not direct database models.
"""

class TimeBlock(BaseModel):
    start: str  # HH:mm format
    end: str  # HH:mm format

class DayHours(BaseModel):
    day: str
    blocks: List[TimeBlock]

class Contact(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    website: Optional[str] = None
    
class SocialMedia(BaseModel):
    platform_name: Optional[str] = None
    link: Optional[str] = None

class PaymentMethod(BaseModel):
    method: str
    minimum: Optional[float] = None

class StaffMember(BaseModel):
    user_id: UUID
    role: str

# --------------------------------------
#               Menu
# --------------------------------------

class MenuItemCreate(BaseModel):
    name: str = Field(..., title='Title', max_length=55, min_length=1)
    description: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    image_url: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    price: float = Field(..., title='Title')
    is_available: bool
    category: Optional[str] = Field(None, title='Title', max_length=55, min_length=1)
    additional_info_menu: List[dict]  # Example: [{"key": "size", "value": "large"}]

    class Config:
        schema_extra = {
            "example": {
                "name": "Cheeseburger",
                "description": "A delicious cheeseburger with lettuce, tomato, and cheese",
                "image_url": "https://example.com/images/cheeseburger.jpg",
                "price": 5.99,
                "is_available": True,
                "category": "Burgers",
                "additional_info_menu": [
                    {"key": "size", "value": "large"},
                    {"key": "ingredients", "value": "beef, lettuce, tomato, cheese"}
                ]
            }
        }

class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(None, title='Title', max_length=55, min_length=1)
    description: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    image_url: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    price: Optional[float] = Field(None, title='Title')
    is_available: Optional[bool] = None
    category: Optional[str] = Field(None, title='Title', max_length=55, min_length=1)
    additional_info_menu: Optional[List[dict]] = None  # Example: [{"key": "size", "value": "large"}]

    class Config:
        schema_extra = {
            "example": {
                "name": "Cheeseburger",
                "description": "A delicious cheeseburger with lettuce, tomato, and cheese",
                "image_url": "https://example.com/images/cheeseburger.jpg",
                "price": 5.99,
                "is_available": True,
                "category": "Burgers",
                "additional_info_menu": [
                    {"key": "size", "value": "large"},
                    {"key": "ingredients", "value": "beef, lettuce, tomato, cheese"}
                ]
            }
        }

class MenuItemOut(BaseModel):
    item_id: UUID
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: float
    is_available: bool
    category: Optional[str] = None
    additional_info_menu: List[dict]  # Example: [{"key": "size", "value": "large"}]

    class Config:
        schema_extra = {
            "example": {
                "item_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Cheeseburger",
                "description": "A delicious cheeseburger with lettuce, tomato, and cheese",
                "image_url": "https://example.com/images/cheeseburger.jpg",
                "price": 5.99,
                "is_available": True,
                "category": "Burgers",
                "additional_info_menu": [
                    {"key": "size", "value": "large"},
                    {"key": "ingredients", "value": "beef, lettuce, tomato, cheese"}
                ]
            }
        }

# --------------------------------------
#               Cafe
# --------------------------------------

class CafeCreate(BaseModel):
    name: str = Field(..., title='Title', max_length=55, min_length=1)
    description: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    image_url: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    faculty: str = Field(..., title='Title', max_length=755, min_length=1)
    location: str = Field(..., title='Title', max_length=755, min_length=1)
    is_open: bool
    opening_hours: List[DayHours]
    contact: Contact
    social_media: List[SocialMedia]
    payment_methods: List[PaymentMethod]
    staff: List[StaffMember]
    menu_items: List[MenuItemCreate]
    additional_info_cafe: List[dict]  # [{"key": "promo", "value": "10% off on Mondays"}]

    class Config:
        schema_extra = {
            "example": {
                "name": "Central Cafe",
                "description": "A popular cafe near the main library.",
                "image_url": "http://example.com/image.jpg",
                "faculty": "Science",
                "location": "Building A, Floor 2",
                "is_open": True,
                "opening_hours": [
                    {"day": "Monday", "blocks": [{"start": "09:00", "end": "17:00"}]},
                ],
                "contact": {
                    "email": "central@cafe.com",
                    "phone_number": "+123456789",
                    "website": "http://centralcafe.com",
                },
                "social_media": [{"platform_name": "Facebook", "link": "http://fb.com/centralcafe"}],
                "payment_methods": [{"method": "Credit Card", "minimum": 10.0}],
                "staff": [{"user_id": "123e4567-e89b-12d3-a456-426614174001", "role": "admin"}],
                "menu_items": [
                    {
                        "name": "Latte",
                        "description": "Creamy and delicious latte.",
                        "image_url": "http://example.com/latte.jpg",
                        "price": 5.0,
                        "is_available": True,
                        "category": "Beverage",
                        "additional_info_menu": [{"key": "size", "value": "large"}],
                    }
                ],
                "additional_info_cafe": [{"key": "promo", "value": "10% off on Mondays"}],
            }
        }

        
class CafeUpdate(BaseModel):
    name: Optional[str] = Field(None, title='Title', max_length=55, min_length=1)
    description: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    image_url: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    faculty: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    location: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    is_open: Optional[bool] = None
    opening_hours: Optional[List[DayHours]] = None
    contact: Optional[Contact] = None
    social_media: Optional[List[SocialMedia]] = None
    payment_methods: Optional[List[PaymentMethod]] = None
    staff: Optional[List[StaffMember]] = None
    menu_items: Optional[List[MenuItemUpdate]] = None
    additional_info_cafe: Optional[List[dict]] = None # [{"key": "promo", "value": "10% off on Mondays"}]

    class Config:
        schema_extra = {
            "example": {
                "name": "Central Cafe",
                "description": "A popular cafe near the main library.",
                "image_url": "http://example.com/image.jpg",
                "faculty": "Science",
                "location": "Building A, Floor 2",
                "is_open": True,
                "opening_hours": [
                    {"day": "Monday", "blocks": [{"start": "09:00", "end": "17:00"}]},
                ],
                "contact": {
                    "email": "central@cafe.com",
                    "phone_number": "+123456789",
                    "website": "http://centralcafe.com",
                },
                "social_media": [{"platform_name": "Facebook", "link": "http://fb.com/centralcafe"}],
                "payment_methods": [{"method": "Credit Card", "minimum": 10.0}],
                "staff": [{"user_id": "123e4567-e89b-12d3-a456-426614174001", "role": "admin"}],
                "menu_items": [
                    {
                        "name": "Latte",
                        "description": "Creamy and delicious latte.",
                        "image_url": "http://example.com/latte.jpg",
                        "price": 5.0,
                        "is_available": True,
                        "category": "Beverage",
                        "additional_info_menu": [{"key": "size", "value": "large"}],
                    }
                ],
                "additional_info_cafe": [{"key": "promo", "value": "10% off on Mondays"}],
            }
        }

class CafeOut(BaseModel):
    cafe_id: UUID
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    faculty: str
    location: str
    is_open: bool
    opening_hours: List[DayHours]
    contact: Contact
    social_media: List[SocialMedia]
    payment_methods: List[PaymentMethod]
    staff: List[StaffMember]
    menu_items: List[MenuItemOut]
    additional_info_cafe: List[dict]  # [{"key": "promo", "value": "10% off on Mondays"}]

    class Config:
        schema_extra = {
            "example": {
                "cafe_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Central Cafe",
                "description": "A popular cafe near the main library.",
                "image_url": "http://example.com/image.jpg",
                "faculty": "Science",
                "location": "Building A, Floor 2",
                "is_open": True,
                "opening_hours": [
                    {"day": "Monday", "blocks": [{"start": "09:00", "end": "17:00"}]},
                ],
                "contact": {
                    "email": "central@cafe.com",
                    "phone_number": "+123456789",
                    "website": "http://centralcafe.com",
                },
                "social_media": [{"platform_name": "Facebook", "link": "http://fb.com/centralcafe"}],
                "payment_methods": [{"method": "Credit Card", "minimum": 10.0}],
                "staff": [{"user_id": "123e4567-e89b-12d3-a456-426614174001", "role": "admin"}],
                "menu_items": [
                    {
                        "item_id": "123e4567-e89b-12d3-a456-426614174002",
                        "name": "Latte",
                        "description": "Creamy and delicious latte.",
                        "image_url": "http://example.com/latte.jpg",
                        "price": 5.0,
                        "is_available": True,
                        "category": "Beverage",
                        "additional_info_menu": [{"key": "size", "value": "large"}],
                    }
                ],
                "additional_info_cafe": [{"key": "promo", "value": "10% off on Mondays"}],
            }
        }

        