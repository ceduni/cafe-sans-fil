from typing import List, Optional
from uuid import UUID, uuid4
from beanie import Document, DecimalAnnotation, Indexed
from pydantic import field_validator, BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime
import re
import unicodedata

"""
This module defines the Pydantic-based models used in the Café application for cafe management,
which are specifically designed for database interaction via the Beanie ODM 
(Object Document Mapper) for MongoDB. These models detail the structure, relationships, 
and constraints of the cafe-related data stored in the database.

Note: These models are intended for direct database interactions related to cafes and are 
different from the API data interchange models.
"""

class TimeBlock(BaseModel):
    start: str = Field(..., description="Start time in HH:mm format.")
    end: str = Field(..., description="End time in HH:mm format.")

    @field_validator('start', 'end')
    @classmethod
    def validate_time_format(cls, time_value):
        try:
            datetime.strptime(time_value, '%H:%M')
        except ValueError:
            raise ValueError("Time must be in HH:mm format.")
        return time_value
    
class Days(str, Enum):
    MONDAY = "Lundi"
    TUESDAY = "Mardi"
    WEDNESDAY = "Mercredi"
    THURSDAY = "Jeudi"
    FRIDAY = "Vendredi"
    SATURDAY = "Samedi"
    SUNDAY = "Dimanche"

class DayHours(BaseModel):
    day: Days = Field(..., description="Day of the week.")
    blocks: List[TimeBlock] = Field(..., description="List of time blocks for the day.")

class Location(BaseModel):
    pavillon: Indexed(str) = Field(..., description="Name or identifier of the pavilion.")
    local: Indexed(str) = Field(..., description="Local identifier within the pavilion.")

class Contact(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Contact email address.")
    phone_number: Optional[str] = Field(None, description="Contact phone number.")
    website: Optional[str] = Field(None, description="Website URL.")

class SocialMedia(BaseModel):
    platform_name: str = Field(..., description="Name of the social media platform.")
    link: str = Field(..., description="Link to the social media profile.")

class PaymentMethod(BaseModel):
    method: str = Field(..., description="Payment method used in the cafe.")
    minimum: Optional[DecimalAnnotation] = Field(None, description="Minimum amount required for this payment method, if any.")
    
class AdditionalInfo(BaseModel):
    type: str = Field(..., description="Type of additional information, e.g., 'promo', 'event'.")
    value: str = Field(..., description="Description or value of the additional information.")
    start: Optional[datetime] = Field(None, description="Start time or date of the additional information.")
    end: Optional[datetime] = Field(None, description="End time or date of the additional information.")

class Role(str, Enum):
    VOLUNTEER = "Bénévole"
    ADMIN = "Admin"
    
class StaffMember(BaseModel):
    username: Indexed(str, unique=True) = Field(..., description="Username of the staff member.")
    role: Role = Field(..., description="Role of the staff member, e.g., 'Bénévole', 'Admin'.")

class MenuItemOption(BaseModel):
    type: str = Field(..., description="Type of the menu item option.")
    value: str = Field(..., description="Value or description of the option.")
    fee: DecimalAnnotation = Field(..., description="Additional fee for this option, if applicable.")

    @field_validator('fee')
    @classmethod
    def validate_fee(cls, fee):
        if fee < DecimalAnnotation(0.0):
            raise ValueError("Fee must be a non-negative value.")
        return fee

class MenuItem(BaseModel):
    item_id: UUID = Field(default_factory=uuid4, description="Unique identifier of the menu item.")
    name: Indexed(str, unique=True) = Field(..., description="Name of the menu item.")
    slug: Indexed(str, unique=True) = Field(None, description="URL-friendly slug for the menu item.")
    tags: List[str] = Field(..., description="List of tags associated with the menu item.")
    description: Indexed(str) = Field(..., description="Description of the menu item.")
    image_url: Optional[str] = Field(None, description="Image URL of the menu item.")
    price: DecimalAnnotation = Field(..., description="Price of the menu item.")
    in_stock: bool = Field(False, description="Availability status of the menu item.")
    category: Indexed(str) = Field(..., description="Category of the menu item.")
    options: List[MenuItemOption] = Field(..., description="List of options available for the menu item.")

    def __init__(self, **data):
        super().__init__(**data)
        self.slug = slugify(self.name)

    @field_validator('price')
    @classmethod
    def validate_price(cls, price):
        if price < DecimalAnnotation(0.0):
            raise ValueError("Price must be a non-negative value.")
        return price
    
class Cafe(Document):
    cafe_id: UUID = Field(default_factory=uuid4)
    name: Indexed(str, unique=True)
    slug: Indexed(str, unique=True) = None
    description: Indexed(str)
    image_url: Optional[str] = None 
    faculty: Indexed(str)
    is_open: bool = False
    status_message: Optional[str] = None
    opening_hours: List[DayHours]
    location: Location
    contact: Contact
    social_media: List[SocialMedia]
    payment_methods: List[PaymentMethod]
    additional_info: List[AdditionalInfo]
    staff: List[StaffMember]
    menu_items: List[MenuItem]
    
    def __init__(self, **data):
        super().__init__(**data)
        self.slug = slugify(self.name)

    class Settings:
        name = "cafes"

def slugify(text):
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    slug = re.sub(r'\W+', '-', text)
    slug = slug.strip('-')
    return slug