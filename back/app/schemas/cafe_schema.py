from typing import List, Optional
from uuid import UUID
from pydantic import field_validator, ConfigDict, BaseModel, Field
from datetime import datetime, timedelta
from beanie import DecimalAnnotation
from app.models.cafe_model import Affiliation, Feature, DayHours, Location, Contact, SocialMedia, PaymentMethod, AdditionalInfo, StaffMember

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
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "username": "janedoe",
            "role": "Bénévole",
        }
    })

class StaffUpdate(BaseModel):
    role: Optional[str] = Field(None, description="Updated role of the staff member.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "role": "Admin",
        }
    })

class StaffOut(BaseModel):
    username: str = Field(..., description="The username of the staff member.")
    role: str = Field(..., description="The role of the staff member within the cafe.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "username": "janedoe",
            "role": "Bénévole",
        }
    })

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
    menu_item_ids: List[UUID] = Field(..., description="List of menu item UUIDs offered by the cafe.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Café Central",
            "features": ["Order"],
            "description": "Un café populaire près de la bibliothèque principale.",
            "logo_url": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.vecteezy.com%2Fsystem%2Fresources%2Fpreviews%2F000%2F585%2F220%2Foriginal%2Fcoffee-cup-logo-template-vector-icon-design.jpg&f=1&nofb=1&ipt=aeea34b58ed1a37dcf59bb11ed370c2e35a2d39c219c47eb5b044c8cf1aad5dc&ipo=images",
            "image_url": "https://media.architecturaldigest.com/photos/5b083c4675a4f940de3da8f1/master/pass/case-study-coffee.jpg",
            "affiliation": {
                "university": "University of Montreal",
                "department": "Droit",
            },
            "location": {
                "pavillon": "Pavillon JEAN-TALON",
                "local": "local B-1234",
                "geometry": {"type": "Point", "coordinates": [45.504, -73.577]}
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
            "social_media": {
                "facebook": "https://www.facebook.com/centralcafe",
            },
            "payment_methods": [{"method": "Carte de Crédit", "minimum": 4.0}],
            "staff": [
                {"username": "cafesansfil", "role": "Admin"}
            ],
            "menu_item_ids": [
                "123e4567-e89b-12d3-a456-426614174001",
                "123e4567-e89b-12d3-a456-426614174002"
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
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Café Central",
            "features": ["Order"],
            "description": "Un café populaire près de la bibliothèque principale.",
            "logo_url": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.vecteezy.com%2Fsystem%2Fresources%2Fpreviews%2F000%2F585%2F220%2Foriginal%2Fcoffee-cup-logo-template-vector-icon-design.jpg&f=1&nofb=1&ipt=aeea34b58ed1a37dcf59bb11ed370c2e35a2d39c219c47eb5b044c8cf1aad5dc&ipo=images",
            "image_url": "https://media.architecturaldigest.com/photos/5b083c4675a4f940de3da8f1/master/pass/case-study-coffee.jpg",
            "affiliation": {
                "university": "University of Montreal",
                "department": "Droit",
            },
            "location": {
                "pavillon": "Pavillon JEAN-TALON",
                "local": "local B-1234",
                "geometry": {"type": "Point", "coordinates": [45.504, -73.577]}
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
            "social_media": {
                "facebook": "https://www.facebook.com/centralcafe",
            },
            "payment_methods": [{"method": "Carte de Crédit", "minimum": 4.0}],
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
    cafe_id: UUID = Field(..., description="Unique identifier of the cafe.")
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
    menu_item_ids: List[UUID] = Field(..., description="List of menu item UUIDs offered by the cafe.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "cafe_id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Café Central",
            "slug": "cafe-central",
            "previous_slugs": ["cafe-central-1", "cafe-central-2"],
            "features": ["Order"],
            "description": "Un café populaire près de la bibliothèque principale.",
            "logo_url": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.vecteezy.com%2Fsystem%2Fresources%2Fpreviews%2F000%2F585%2F220%2Foriginal%2Fcoffee-cup-logo-template-vector-icon-design.jpg&f=1&nofb=1&ipt=aeea34b58ed1a37dcf59bb11ed370c2e35a2d39c219c47eb5b044c8cf1aad5dc&ipo=images",
            "image_url": "https://media.architecturaldigest.com/photos/5b083c4675a4f940de3da8f1/master/pass/case-study-coffee.jpg",
            "affiliation": {
                "university": "University of Montreal",
                "department": "Droit",
            },
            "location": {
                "pavillon": "Pavillon JEAN-TALON",
                "local": "local B-1234",
                "geometry": {"type": "Point", "coordinates": [45.504, -73.577]}
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
            "social_media": {
                "facebook": "https://www.facebook.com/centralcafe",
            },
            "payment_methods": [{"method": "Carte de Crédit", "minimum": 4.0}],
            "staff": [
                {"username": "johndoe", "role": "Admin"},
                {"username": "janedoe", "role": "Admin"},
                {"username": "johndoe2", "role": "Bénévole"},
                {"username": "janedoe2", "role": "Bénévole"},
                {"username": "johndoe3", "role": "Bénévole"},
                {"username": "janedoe3", "role": "Bénévole"}
            ],
            "menu_item_ids": [
                "123e4567-e89b-12d3-a456-426614174001",
                "123e4567-e89b-12d3-a456-426614174002"
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

class CafeShortOut(BaseModel):
    cafe_id: UUID = Field(..., description="Unique identifier of the cafe.")
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
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "cafe_id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Café Central",
            "slug": "cafe-central",
            "previous_slugs": ["cafe-central-1", "cafe-central-2"],
            "features": ["Order"],
            "description": "Un café populaire près de la bibliothèque principale.",
            "logo_url": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.vecteezy.com%2Fsystem%2Fresources%2Fpreviews%2F000%2F585%2F220%2Foriginal%2Fcoffee-cup-logo-template-vector-icon-design.jpg&f=1&nofb=1&ipt=aeea34b58ed1a37dcf59bb11ed370c2e35a2d39c219c47eb5b044c8cf1aad5dc&ipo=images",
            "image_url": "https://media.architecturaldigest.com/photos/5b083c4675a4f940de3da8f1/master/pass/case-study-coffee.jpg",
            "affiliation": {
                "university": "University of Montreal",
                "department": "Droit",
            },
            "location": {
                "pavillon": "Pavillon JEAN-TALON",
                "local": "local B-1234",
                "geometry": {"type": "Point", "coordinates": [45.504, -73.577]}
            },
            "is_open": True,
            "opening_hours": [
                {"day": "Lundi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Mardi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Mercredi", "blocks": [{"start": "09:00", "end": "12:00"}, {"start": "13:00", "end": "17:00"}]},
                {"day": "Jeudi", "blocks": [{"start": "09:00", "end": "17:00"}]},
                {"day": "Vendredi", "blocks": [{"start": "10:00", "end": "11:00"}, {"start": "12:00", "end": "17:00"}]}
            ],
            "payment_methods": [{"method": "Carte de Crédit", "minimum": 4.0}],
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
