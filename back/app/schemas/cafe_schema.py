from typing import List, Optional
from pydantic import field_validator, BaseModel, Field
from beanie import DecimalAnnotation, PydanticObjectId
from app.models.cafe_model import Affiliation, Feature, DayHours, Location, Contact, SocialMedia, PaymentMethod, AdditionalInfo, StaffMember
from app.models.menu_model import MenuItem, MenuItemEmbedded

"""
This module defines the Pydantic-based schemas for cafe operations in the Café application. 
These schemas are utilized for request and response validation, serialization, 
and documentation specific to cafe listings, details, and management.

Note: These models are for API data interchange related to cafes and not direct database models.
"""

# --------------------------------------
#               Staff
# --------------------------------------

class StaffCreate(BaseModel):
    username: str = Field(..., description="The username of the staff member.")
    role: str = Field(..., description="The role of the staff member within the cafe.")

class StaffUpdate(BaseModel):
    role: Optional[str] = Field(None, description="Updated role of the staff member.")

class StaffOut(BaseModel):
    username: str = Field(..., description="The username of the staff member.")
    role: str = Field(..., description="The role of the staff member within the cafe.")

# --------------------------------------
#               Cafe
# --------------------------------------

class CafeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Name of the cafe.")
    features: List[Feature] = Field(..., description="Features of the cafe.")
    description: str = Field(..., min_length=1, max_length=255, description="Description of the cafe.")
    logo_url: Optional[str] = Field(None, max_length=755, description="Logo URL of the cafe.")
    image_url: Optional[str] = Field(None, max_length=755, description="Image URL of the cafe.")
    affiliation: Affiliation = Field(..., description="Affiliation of the cafe.")
    is_open: bool = Field(..., description="Indicates if the cafe is currently open.")
    status_message: Optional[str] = Field(None, max_length=50, description="Status message about the cafe.")
    opening_hours: List[DayHours] = Field(..., description="Opening hours of the cafe.")
    location: Location = Field(..., description="Location details of the cafe.")
    contact: Contact = Field(..., description="Contact information of the cafe.")
    social_media: SocialMedia = Field(..., description="Social media profiles of the cafe.")
    payment_methods: List[PaymentMethod] = Field(..., description="Accepted payment methods at the cafe.")
    additional_info: List[AdditionalInfo] = Field(..., description="Additional information about the cafe.")
    staff: List[StaffMember] = Field(..., description="Staff members of the cafe.")
    menu_item_ids: List[PydanticObjectId] = Field(..., description="List of menu item IDs offered by the cafe.")


class CafeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Updated name of the cafe.")
    features: Optional[List[Feature]] = Field(None, description="Updated features of the cafe.")
    description: Optional[str] = Field(None, min_length=1, max_length=255, description="Updated description of the cafe.")
    logo_url: Optional[str] = Field(None, max_length=755, description="Logo URL of the cafe.")
    image_url: Optional[str] = Field(None, max_length=755, description="Image URL of the cafe.")
    affiliation: Affiliation = Field(..., description="Affiliation of the cafe.")
    is_open: Optional[bool] = Field(None, description="Updated open status of the cafe.")
    status_message: Optional[str] = Field(None, max_length=50, description="Updated status message of the cafe.")
    opening_hours: Optional[List[DayHours]] = Field(None, description="Updated opening hours of the cafe.")
    location: Optional[Location] = Field(None, description="Updated location details of the cafe.")
    contact: Optional[Contact] = Field(None, description="Updated contact information of the cafe.")
    social_media: Optional[SocialMedia] = Field(None, description="Updated social media profiles of the cafe.")
    payment_methods: Optional[List[PaymentMethod]] = Field(None, description="Updated payment methods accepted at the cafe.")
    additional_info: Optional[List[AdditionalInfo]] = Field(None, description="Updated additional information about the cafe.")


class CafeOut(BaseModel):
    id: PydanticObjectId = Field(..., description="Unique identifier of the cafe.")
    name: str = Field(..., description="Name of the cafe.")
    slug: str = Field(..., description="Slug of the cafe.")
    previous_slugs: List[str] = Field(None, description="Previous slugs of the cafe.")
    features: List[Feature] = Field(..., description="Features of the cafe.")
    description: str = Field(..., description="Description of the cafe.")
    logo_url: Optional[str] = Field(None, max_length=755, description="Logo URL of the cafe.")
    image_url: Optional[str] = Field(None, max_length=755, description="Image URL of the cafe.")
    affiliation: Affiliation = Field(..., description="Affiliation of the cafe.")
    is_open: bool = Field(..., description="Open status of the cafe.")
    status_message: Optional[str] = Field(None, description="Status message about the cafe.")
    opening_hours: List[DayHours] = Field(..., description="Opening hours of the cafe.")
    location: Location = Field(..., description="Location details of the cafe.")
    contact: Contact = Field(..., description="Contact information of the cafe.")
    social_media: SocialMedia = Field(..., description="Social media profiles of the cafe.")
    payment_methods: List[PaymentMethod] = Field(..., description="Payment methods accepted at the cafe.")
    additional_info: List[AdditionalInfo] = Field(..., description="Additional information about the cafe.")
    staff: List[StaffMember] = Field(..., description="Staff members of the cafe.")
    menu_items: List[MenuItemEmbedded] = Field(..., description="List of menu items offered by the cafe.")


class CafeShortOut(BaseModel):
    id: PydanticObjectId = Field(..., description="Unique identifier of the cafe.")
    name: str = Field(..., description="Name of the cafe.")
    slug: str = Field(..., description="Slug of the cafe.")
    previous_slugs: List[str] = Field(None, description="Previous slugs of the cafe.")
    features: List[Feature] = Field(..., description="Features of the cafe.")
    description: str = Field(..., description="Description of the cafe.")
    logo_url: Optional[str] = Field(None, max_length=755, description="Logo URL of the cafe.")
    image_url: Optional[str] = Field(None, max_length=755, description="Image URL of the cafe.")
    affiliation: Affiliation = Field(..., description="Affiliation of the cafe.")
    is_open: bool = Field(..., description="Open status of the cafe.")
    status_message: Optional[str] = Field(None, description="Status message about the cafe.")
    opening_hours: List[DayHours] = Field(..., description="Opening hours of the cafe.")
    location: Location = Field(..., description="Location details of the cafe.")
    payment_methods: List[PaymentMethod] = Field(..., description="Payment methods accepted at the cafe.")
    additional_info: List[AdditionalInfo] = Field(..., description="Additional information about the cafe.")
