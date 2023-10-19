from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import List, Optional
from datetime import datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    udem_email: EmailStr = Field(..., unique=True)
    first_name: str = Field(...)
    last_name: str = Field(...)
    roles: List[dict] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "3d2e3d2e3d2e3d2e3d2e3d2e",
                "udem_email": "john.doe@umontreal.ca",
                "first_name": "John",
                "last_name": "Doe",
                "roles": {
                    "cafe_id": "5f897f7d7d6d6d6d6d6d6d6d",
                    "role_type": "benevole"
                }
            }
        }


class Cafe(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    faculty: str = Field(...)
    location: str = Field(...)
    email: EmailStr = Field(...)
    phone_number: Optional[str]
    website: Optional[str]
    facebook: Optional[str]
    instagram: Optional[str]
    image_url: Optional[str]
    is_open: bool = Field(...)
    opening_hours: List[dict] = Field(...)
    payment_methods: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "5f897f7d7d6d6d6d6d6d6d6d",
                "name": "Tore et fraction",
                "description": "Café 100% bénévoles, vue du coucher de soleil magnifique, on remplit votre tasse pour 0,50$.",
                "faculty": "INFORMATIQUE ET RECHERCHE OPÉRATIONNELLE, MATHÉMATIQUES ET STATISTIQUES",
                "location": "PAVILLON ANDRÉ-AISENSTADT, LOCAL AA-1221",
                "email": "toreetfraction@gmail.com",
                "phone_number": "(514)-834-4601",
                "facebook": "https://www.facebook.com/CafeToreetFraction",
                "instagram": "https://www.instagram.com/toreetfraction/",
                "image_url": "https://i.imgur.com/hsihihdiz.jpg",
                "is_open": True,
                "opening_hours": [{
                    "monday": {
                        "open": "08:00",
                        "close": "18:00"
                    },
                    "tuesday": {
                        "open": "08:00",
                        "close": "18:00"
                    },
                    "wednesday": {
                        "open": "08:00",
                        "close": "18:00"
                    },
                    "thursday": {
                        "open": "08:00",
                        "close": "18:00"
                    },
                    "friday": {
                        "open": "08:00",
                        "close": "18:00"
                    },
                    "saturday": {
                        "open": None,
                        "close": None
                    },
                    "sunday": {
                        "open": None,
                        "close": None
                    }
                }],
                "payment_methods": [
                    "comptant",
                    "débit",
                    "crédit"
                ]
            }
        }


class MenuItem(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    cafe_id: PyObjectId = Field(...)
    name: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    image_url: Optional[str]
    is_available: bool = Field(...)
    category: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "9d8e9d8e9d8e9d8e9d8e9d8e",
                "cafe_id": "5f897f7d7d6d6d6d6d6d6d6d",
                "name": "Café au lait",
                "description": "Café au lait, 2 laits, 2 sucres",
                "price": 1.5,
                "image_url": "https://i.imgur.com/hsihihdiz.jpg",
                "is_available": True,
                "category": "boisson"
            }
        }


class Order(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId = Field(...)
    cafe_id: PyObjectId = Field(...)
    items: List[dict] = Field(...)
    total_price: float = Field(...)
    status: str = Field(...)
    order_timestamp: datetime = datetime.now()
    pickup_timestamp: datetime = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "2d2e3d2e3d2e3d2e3d2e3d2e",
                "user_id": "3d2e3d2e3d2e3d2e3d2e3d2e",
                "cafe_id": "5f897f7d7d6d6d6d6d6d6d6d",
                "items": [{
                    "item_id": "9d8e9d8e9d8e9d8e9d8e9d8e",
                    "quantity": 2,
                    "item_price": 1.5
                }],
                "total_price": 3.0,
                "status": "active",
                "order_timestamp": "2023-10-20T20:20:20.000Z",
                "pickup_timestamp": "2023-10-20T20:40:20.000Z"
            }
        }
