from typing import List, Optional

from beanie import DecimalAnnotation, PydanticObjectId
from pydantic import BaseModel, Field, field_validator

from app.cafe.models import (
    AdditionalInfo,
    Affiliation,
    Contact,
    DayHours,
    Feature,
    Location,
    PaymentMethod,
    SocialMedia,
    StaffMember,
)
from app.menu.models import MenuItem, MenuItemEmbedded

# --------------------------------------
#               Staff
# --------------------------------------


class StaffCreate(BaseModel):
    username: str
    role: str


class StaffUpdate(BaseModel):
    role: Optional[str] = None


class StaffOut(BaseModel):
    username: str
    role: str


# --------------------------------------
#               Cafe
# --------------------------------------


class CafeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    features: List[Feature]
    description: str = Field(..., min_length=1, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=755)
    image_url: Optional[str] = Field(None, max_length=755)
    affiliation: Affiliation
    is_open: bool
    status_message: Optional[str] = Field(None, max_length=50)
    opening_hours: List[DayHours]
    location: Location
    contact: Contact
    social_media: SocialMedia
    payment_methods: List[PaymentMethod]
    additional_info: List[AdditionalInfo]
    staff: List[StaffMember]
    menu_item_ids: List[PydanticObjectId]


class CafeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    features: Optional[List[Feature]] = None
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=755)
    image_url: Optional[str] = Field(None, max_length=755)
    affiliation: Optional[Affiliation] = None
    is_open: Optional[bool] = None
    status_message: Optional[str] = Field(None, max_length=50)
    opening_hours: Optional[List[DayHours]] = None
    location: Optional[Location] = None
    contact: Optional[Contact] = None
    social_media: Optional[SocialMedia] = None
    payment_methods: Optional[List[PaymentMethod]] = None
    additional_info: Optional[List[AdditionalInfo]] = None


class CafeOut(BaseModel):
    id: PydanticObjectId
    name: str
    slug: str
    previous_slugs: Optional[List[str]] = None
    features: List[Feature]
    description: str
    logo_url: Optional[str] = Field(None, max_length=755)
    image_url: Optional[str] = Field(None, max_length=755)
    affiliation: Affiliation
    is_open: bool
    status_message: Optional[str] = Field(None, max_length=50)
    opening_hours: List[DayHours]
    location: Location
    contact: Contact
    social_media: SocialMedia
    payment_methods: List[PaymentMethod]
    additional_info: List[AdditionalInfo]
    staff: List[StaffMember]
    menu_items: List[MenuItemEmbedded]


class CafeShortOut(BaseModel):
    id: PydanticObjectId
    name: str
    slug: str
    previous_slugs: Optional[List[str]] = None
    features: List[Feature]
    description: str
    logo_url: Optional[str] = Field(None, max_length=755)
    image_url: Optional[str] = Field(None, max_length=755)
    affiliation: Affiliation
    is_open: bool
    status_message: Optional[str] = Field(None, max_length=50)
    opening_hours: List[DayHours]
    location: Location
    payment_methods: List[PaymentMethod]
    additional_info: List[AdditionalInfo]
