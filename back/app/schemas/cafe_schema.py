from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

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

class MenuItem(BaseModel):
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

class Cafe(BaseModel):
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
    menu_items: List[MenuItem]
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