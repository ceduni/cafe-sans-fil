from typing import List, Optional
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field

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
    item_id: UUID = Field(default_factory=uuid4, unique=True)
    name: str
    description: Optional[str] = None 
    image_url: Optional[str] = None 
    price: float
    is_available: bool = False
    category: Optional[str] = None 
    additional_info_menu: List[dict]  # Example: [{"key": "size", "value": "large"}]

class Cafe(Document):
    cafe_id: UUID = Field(default_factory=uuid4, unique=True)
    name: Indexed(str)
    description: Optional[str] = None 
    image_url: Optional[str] = None 
    faculty: str
    location: Indexed(str)
    is_open: bool = False
    opening_hours: List[DayHours]
    contact: Contact
    social_media: List[SocialMedia]
    payment_methods: List[PaymentMethod]
    staff: List[StaffMember]
    menu_items: List[MenuItem]
    additional_info_cafe: List[dict]  # [{"key": "promo", "value": "10% off on Mondays"}]

    class Collection:
        name = "cafes"
