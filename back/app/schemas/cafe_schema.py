from typing import List, Optional
from uuid import UUID
from pydantic import ConfigDict, BaseModel, Field
from datetime import datetime, timedelta
from decimal import Decimal
from app.models.cafe_model import DayHours, Location, Contact, SocialMedia, PaymentMethod, AdditionalInfo, StaffMember, MenuItemOption

"""
This module defines the Pydantic-based schemas for cafe operations in the Café application. 
These schemas are utilized for request and response validation, serialization, 
and documentation specific to cafe listings, details, and management.

Note: These models are for API data interchange related to cafes and not direct database models.
"""

# --------------------------------------
#               Menu
# --------------------------------------

class MenuItemCreate(BaseModel):
    name: str = Field(..., title='Title', max_length=55, min_length=1)
    tags: List[str]
    description: str = Field(..., title='Title', max_length=755, min_length=1)
    image_url: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    price: Decimal = Field(..., title='Title')
    is_available: bool
    category: str = Field(None, title='Title', max_length=55, min_length=1)
    options: List[MenuItemOption]
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Cheeseburger",
            "tags": ["Rapide", "Savoureux"],
            "description": "Un délicieux cheeseburger avec laitue, tomate et fromage",
            "image_url": "https://thedelightfullaugh.com/wp-content/uploads/2020/09/smashed-double-cheeseburger.jpg",
            "price": 5.99,
            "is_available": True,
            "category": "Burgers",
            "options": [
                {"type": "taille", "value": "grand", "fee": 0.5},
                {"type": "ingrédients", "value": "bœuf", "fee": 0},
                {"type": "ingrédients", "value": "laitue", "fee": 0},
                {"type": "ingrédients", "value": "tomate", "fee": 0},
                {"type": "ingrédients", "value": "fromage", "fee": 0}
            ]
        }
    })

class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(None, title='Title', max_length=55, min_length=1)
    tags: Optional[List[str]] = None
    description: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    image_url: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    price: Optional[Decimal] = Field(None, title='Title')
    is_available: Optional[bool] = None
    category: Optional[str] = Field(None, title='Title', max_length=55, min_length=1)
    options: Optional[List[MenuItemOption]] = None
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Cheeseburger Spécial",
            "tags": ["Gourmet", "Nouveau"],
            "description": "Cheeseburger gourmet avec bacon et sauce spéciale",
            "image_url": "https://thedelightfullaugh.com/wp-content/uploads/2020/09/smashed-double-cheeseburger.jpg",
            "price": 7.99,
            "is_available": False,
            "category": "Burgers Spéciaux",
            "options": [
                {"type": "épice", "value": "piquant", "fee": 0.75},
                {"type": "supplément", "value": "bacon", "fee": 1.0}
            ]
        }
    })

class MenuItemOut(BaseModel):
    item_id: UUID
    name: str
    tags: List[str]
    description: str
    image_url: Optional[str] = None
    price: Decimal
    is_available: bool
    category: str
    options: List[MenuItemOption]
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "item_id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Cheeseburger",
            "tags": ["Classique", "Fromage"],
            "description": "Un cheeseburger classique avec une tranche de fromage fondant",
            "image_url": "https://thedelightfullaugh.com/wp-content/uploads/2020/09/smashed-double-cheeseburger.jpg",
            "price": 5.99,
            "is_available": True,
            "category": "Burgers",
            "options": [
                {"type": "taille", "value": "moyen", "fee": 0.0},
                {"type": "sans oignon", "value": "oui", "fee": 0.0}
            ]
        }
    })

# --------------------------------------
#               Cafe
# --------------------------------------

class CafeCreate(BaseModel):
    name: str = Field(..., title='Title', max_length=55, min_length=1)
    description: str = Field(..., title='Title', max_length=755, min_length=1)
    image_url: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    faculty: str = Field(..., title='Title', max_length=55, min_length=1)
    is_open: bool
    status_message = Optional[str] = Field(None, title='Title', max_length=50, min_length=1)
    opening_hours: List[DayHours]
    location: Location
    contact: Contact
    social_media: List[SocialMedia]
    payment_methods: List[PaymentMethod]
    additional_info: List[AdditionalInfo]
    staff: List[StaffMember]
    menu_items: List[MenuItemCreate]
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Café Central",
            "description": "Un café populaire près de la bibliothèque principale.",
            "image_url": "https://media.architecturaldigest.com/photos/5b083c4675a4f940de3da8f1/master/pass/case-study-coffee.jpg",
            "faculty": "Science",
            "location": {
                "pavillon": "Pavillon JEAN-TALON",
                "local": "local B-1234"
            },
            "is_open": True,
            "opening_hours": [
                {"day": "Lundi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Mardi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Mercredi", "blocks": [{"start": "09:00", "end": "12:00"}, {"start": "13:00", "end": "17:00"}]},
                {"day": "Jeudi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Vendredi", "blocks": [{"start": "10:00", "end": "11:00"}, {"start": "12:00", "end": "17:00"}]}
            ],
            "contact": {
                "email": "central@cafe.com",
                "phone_number": "+123456789",
                "website": "http://centralcafe.com"
            },
            "social_media": [{"platform_name": "Facebook", "link": "http://fb.com/centralcafe"}],
            "payment_methods": [{"method": "Carte de Crédit", "minimum": 4.0}],
            "staff": [
                {"user_id": "15df2842-fc31-4107-99bf-3cb7b0b5baf5", "role": "Admin"},
                {"user_id": "3c0cda2b-26f3-4cc8-8e84-0c81bf84e8f9", "role": "Admin"},
                {"user_id": "a1e63c28-7e5b-4d12-8cf2-8c7875191d2b", "role": "Bénévole"},
                {"user_id": "5a0e7b25-1722-41aa-8eeb-25dfedc2c1ae", "role": "Bénévole"},
                {"user_id": "9c42c791-4b0a-4170-bb8a-2c1f4462cf33", "role": "Bénévole"},
                {"user_id": "e8c5de06-7d98-4d66-89a3-8c37e3b16bd5", "role": "Bénévole"}
            ],
            "menu_items": [
                {
                    "name": "Cheeseburger",
                    "tags": ["Rapide", "Savoureux"],
                    "description": "Un délicieux cheeseburger avec laitue, tomate et fromage",
                    "image_url": "https://thedelightfullaugh.com/wp-content/uploads/2020/09/smashed-double-cheeseburger.jpg",
                    "price": 5.99,
                    "is_available": True,
                    "category": "Burgers",
                    "options": [
                        {"type": "taille", "value": "grand", "fee": 0.5},
                        {"type": "ingrédients", "value": "bœuf", "fee": 0},
                        {"type": "ingrédients", "value": "laitue", "fee": 0},
                        {"type": "ingrédients", "value": "tomate", "fee": 0},
                        {"type": "ingrédients", "value": "fromage", "fee": 0}
                    ]
                },
                {
                    "name": "Chicken Caesar Salad",
                    "tags": ["Léger", "Fraîcheur"],
                    "description": "Une salade César avec du poulet grillé, de la laitue romaine et de la vinaigrette César",
                    "image_url": None,
                    "price": 7.99,
                    "is_available": False,
                    "category": "Salads",
                    "options": []
                }
            ],
            "additional_info": [
                {
                    "type": "promo",
                    "value": "10% de réduction les lundis",
                    "start": datetime.now() - timedelta(hours=5),
                    "end": datetime.now() + timedelta(minutes=30)
                }
            ]
        }
    })
    
class CafeUpdate(BaseModel):
    name: Optional[str] = Field(None, title='Title', max_length=55, min_length=1)
    description: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    image_url: Optional[str] = Field(None, title='Title', max_length=755, min_length=1)
    faculty: Optional[str] = Field(None, title='Title', max_length=55, min_length=1)
    is_open: Optional[bool] = None
    status_message = Optional[str] = Field(None, title='Title', max_length=50, min_length=1)
    opening_hours: Optional[List[DayHours]] = None
    location: Optional[Location] = None
    contact: Optional[Contact] = None
    social_media: Optional[List[SocialMedia]] = None
    payment_methods: Optional[List[PaymentMethod]] = None
    additional_info: Optional[List[AdditionalInfo]] = None
    staff: Optional[List[StaffMember]] = None
    menu_items: Optional[List[MenuItemUpdate]] = None
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Café Central",
            "description": "Un café populaire près de la bibliothèque principale.",
            "image_url": "https://media.architecturaldigest.com/photos/5b083c4675a4f940de3da8f1/master/pass/case-study-coffee.jpg",
            "faculty": "Science",
            "location": {
                "pavillon": "Pavillon JEAN-TALON",
                "local": "local B-1234"
            },
            "is_open": True,
            "opening_hours": [
                {"day": "Lundi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Mardi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Mercredi", "blocks": [{"start": "09:00", "end": "12:00"}, {"start": "13:00", "end": "17:00"}]},
                {"day": "Jeudi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Vendredi", "blocks": [{"start": "10:00", "end": "11:00"}, {"start": "12:00", "end": "17:00"}]}
            ],
            "contact": {
                "email": "central@cafe.com",
                "phone_number": "+123456789",
                "website": "http://centralcafe.com"
            },
            "social_media": [{"platform_name": "Facebook", "link": "http://fb.com/centralcafe"}],
            "payment_methods": [{"method": "Carte de Crédit", "minimum": 4.0}],
            "staff": [
                {"user_id": "15df2842-fc31-4107-99bf-3cb7b0b5baf5", "role": "Admin"},
                {"user_id": "3c0cda2b-26f3-4cc8-8e84-0c81bf84e8f9", "role": "Admin"},
                {"user_id": "a1e63c28-7e5b-4d12-8cf2-8c7875191d2b", "role": "Bénévole"},
                {"user_id": "5a0e7b25-1722-41aa-8eeb-25dfedc2c1ae", "role": "Bénévole"},
                {"user_id": "9c42c791-4b0a-4170-bb8a-2c1f4462cf33", "role": "Bénévole"},
                {"user_id": "e8c5de06-7d98-4d66-89a3-8c37e3b16bd5", "role": "Bénévole"}
            ],
            "menu_items": [
                {
                    "name": "Cheeseburger",
                    "tags": ["Rapide", "Savoureux"],
                    "description": "Un délicieux cheeseburger avec laitue, tomate et fromage",
                    "image_url": "https://thedelightfullaugh.com/wp-content/uploads/2020/09/smashed-double-cheeseburger.jpg",
                    "price": 5.99,
                    "is_available": True,
                    "category": "Burgers",
                    "options": [
                        {"type": "taille", "value": "grand", "fee": 0.5},
                        {"type": "ingrédients", "value": "bœuf", "fee": 0},
                        {"type": "ingrédients", "value": "laitue", "fee": 0},
                        {"type": "ingrédients", "value": "tomate", "fee": 0},
                        {"type": "ingrédients", "value": "fromage", "fee": 0}
                    ]
                },
                {
                    "name": "Chicken Caesar Salad",
                    "tags": ["Léger", "Fraîcheur"],
                    "description": "Une salade César avec du poulet grillé, de la laitue romaine et de la vinaigrette César",
                    "image_url": None,
                    "price": 7.99,
                    "is_available": False,
                    "category": "Salads",
                    "options": []
                }
            ],
            "additional_info": [
                {
                    "type": "promo",
                    "value": "10% de réduction les lundis",
                    "start": datetime.now() - timedelta(hours=5),
                    "end": datetime.now() + timedelta(minutes=30)
                }
            ]
        }
    })

class CafeOut(BaseModel):
    cafe_id: UUID
    name: str
    description: str
    image_url: Optional[str] = None
    faculty: str
    is_open: bool
    status_message = Optional[str] = None
    opening_hours: List[DayHours]
    location: Location
    contact: Contact
    social_media: List[SocialMedia]
    payment_methods: List[PaymentMethod]
    additional_info: List[AdditionalInfo]
    staff: List[StaffMember]
    menu_items: List[MenuItemOut]
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "cafe_id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Café Central",
            "description": "Un café populaire près de la bibliothèque principale.",
            "image_url": "https://media.architecturaldigest.com/photos/5b083c4675a4f940de3da8f1/master/pass/case-study-coffee.jpg",
            "faculty": "Science",
            "location": {
                "pavillon": "Pavillon JEAN-TALON",
                "local": "local B-1234"
            },
            "is_open": True,
            "opening_hours": [
                {"day": "Lundi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Mardi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Mercredi", "blocks": [{"start": "09:00", "end": "12:00"}, {"start": "13:00", "end": "17:00"}]},
                {"day": "Jeudi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Vendredi", "blocks": [{"start": "10:00", "end": "11:00"}, {"start": "12:00", "end": "17:00"}]}
            ],
            "contact": {
                "email": "central@cafe.com",
                "phone_number": "+123456789",
                "website": "http://centralcafe.com"
            },
            "social_media": [{"platform_name": "Facebook", "link": "http://fb.com/centralcafe"}],
            "payment_methods": [{"method": "Carte de Crédit", "minimum": 4.0}],
            "staff": [
                {"user_id": "15df2842-fc31-4107-99bf-3cb7b0b5baf5", "role": "Admin"},
                {"user_id": "3c0cda2b-26f3-4cc8-8e84-0c81bf84e8f9", "role": "Admin"},
                {"user_id": "a1e63c28-7e5b-4d12-8cf2-8c7875191d2b", "role": "Bénévole"},
                {"user_id": "5a0e7b25-1722-41aa-8eeb-25dfedc2c1ae", "role": "Bénévole"},
                {"user_id": "9c42c791-4b0a-4170-bb8a-2c1f4462cf33", "role": "Bénévole"},
                {"user_id": "e8c5de06-7d98-4d66-89a3-8c37e3b16bd5", "role": "Bénévole"}
            ],
            "menu_items": [
                {
                    "item_id": "123e4567-e89b-12d3-a456-426614174001",
                    "name": "Cheeseburger",
                    "tags": ["Rapide", "Savoureux"],
                    "description": "Un délicieux cheeseburger avec laitue, tomate et fromage",
                    "image_url": "https://thedelightfullaugh.com/wp-content/uploads/2020/09/smashed-double-cheeseburger.jpg",
                    "price": 5.99,
                    "is_available": True,
                    "category": "Burgers",
                    "options": [
                        {"type": "taille", "value": "grand", "fee": 0.5},
                        {"type": "ingrédients", "value": "bœuf", "fee": 0},
                        {"type": "ingrédients", "value": "laitue", "fee": 0},
                        {"type": "ingrédients", "value": "tomate", "fee": 0},
                        {"type": "ingrédients", "value": "fromage", "fee": 0}
                    ]
                },
                {
                    "item_id": "123e4567-e89b-12d3-a456-426614174002",
                    "name": "Chicken Caesar Salad",
                    "tags": ["Léger", "Fraîcheur"],
                    "description": "Une salade César avec du poulet grillé, de la laitue romaine et de la vinaigrette César",
                    "image_url": None,
                    "price": 7.99,
                    "is_available": False,
                    "category": "Salads",
                    "options": []
                }
            ],
            "additional_info": [
                {
                    "type": "promo",
                    "value": "10% de réduction les lundis",
                    "start": datetime.now() - timedelta(hours=5),
                    "end": datetime.now() + timedelta(minutes=30)
                }
            ]
        }
    })
