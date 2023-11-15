from typing import List, Optional
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime

"""
This module defines the Pydantic-based models used in the Café application for cafe management,
which are specifically designed for database interaction via the Beanie ODM 
(Object Document Mapper) for MongoDB. These models detail the structure, relationships, 
and constraints of the cafe-related data stored in the database.

Note: These models are intended for direct database interactions related to cafes and are 
different from the API data interchange models.
"""

class TimeBlock(BaseModel):
    start: str  # HH:mm format
    end: str  # HH:mm format

class DayHours(BaseModel):
    day: str
    blocks: List[TimeBlock]

class Location(BaseModel):
    pavillon: Indexed(str)
    local: Indexed(str)

class Contact(BaseModel):
    email: Optional[EmailStr] = None 
    phone_number: Optional[str] = None 
    website: Optional[str] = None 
        
class SocialMedia(BaseModel):
    platform_name: str
    link: str

class PaymentMethod(BaseModel):
    method: str
    minimum: Optional[float] = None

class AdditionalInfo(BaseModel):
    type: str
    value: str
    start: Optional[datetime] = None 
    end: Optional[datetime] = None 

class Role(str, Enum):
    VOLUNTEER = "Bénévole"
    ADMIN = "Admin"
    
class StaffMember(BaseModel):
    user_id: UUID
    role: Role

class MenuItemOption(BaseModel):
    type: str
    value: str
    fee: float

class MenuItem(BaseModel):
    item_id: UUID = Field(default_factory=uuid4, unique=True)
    name: Indexed(str, unique=True)
    tags: List[str]
    description: Indexed(str) 
    image_url: Optional[str] = None 
    price: Indexed(float)
    is_available: bool = False
    category: Indexed(str)
    options: List[MenuItemOption]

class Cafe(Document):
    cafe_id: UUID = Field(default_factory=uuid4, unique=True)
    name: Indexed(str, unique=True)
    description: Indexed(str)
    image_url: Optional[str] = None 
    faculty: Indexed(str)
    is_open: bool = False
    opening_hours: List[DayHours]
    location: Location
    contact: Contact
    social_media: List[SocialMedia]
    payment_methods: List[PaymentMethod]
    additional_info: List[AdditionalInfo]
    staff: List[StaffMember]
    menu_items: List[MenuItem]

    class Settings:
        name = "cafes"
