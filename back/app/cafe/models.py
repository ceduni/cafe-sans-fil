"""
Module for handling cafe-related models.
"""

import re
from datetime import datetime
from typing import List, Optional

import pymongo
from beanie import DecimalAnnotation, Document, View
from pydantic import BaseModel, Field, field_validator
from pymongo import IndexModel

from app.cafe.enums import Days, Feature, Role
from app.cafe.helper import slugify, time_blocks_overlap
from app.cafe_menu.models import MenuCategory, MenuView, MenuViewOut
from app.models import Id, IdAlias


class Affiliation(BaseModel):
    """Model for university affiliation."""

    university: str = Field(..., min_length=1)
    faculty: str = Field(..., min_length=1)


class TimeBlock(BaseModel):
    """Model for time blocks."""

    start: str = Field(..., min_length=1)
    end: str = Field(..., min_length=1)

    @field_validator("start", "end")
    @classmethod
    def validate_time_format(cls, time_value):
        """Validate time format."""
        try:
            datetime.strptime(time_value, "%H:%M")
        except ValueError:
            raise ValueError("Time must be in HH:mm format.")
        return time_value


class DayHours(BaseModel):
    """Model for daily hours."""

    day: Days
    blocks: List[TimeBlock]


class Geometry(BaseModel):
    """Model for geographic location."""

    type: str = Field(..., min_length=1)
    coordinates: List[float] = Field(..., min_length=1)


class Location(BaseModel):
    """Model for location."""

    pavillon: str = Field(..., min_length=1)
    local: str = Field(..., min_length=1)
    geometry: Optional[Geometry] = None


class Contact(BaseModel):
    """Model for contact information."""

    email: Optional[str] = None
    phone_number: Optional[str] = None
    website: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        """Validate email address."""
        if v is None or v == "":
            return None
        email_regex = re.compile(r"^\w+[\w.-]*@\w+[\w.-]+\.\w+$")
        if not email_regex.match(v):
            raise ValueError("Invalid email address")
        return v


class SocialMedia(BaseModel):
    """Model for social media links."""

    facebook: Optional[str] = None
    instagram: Optional[str] = None
    x: Optional[str] = None


class PaymentMethod(BaseModel):
    """Model for payment methods."""

    method: str = Field(..., min_length=1)
    minimum: Optional[DecimalAnnotation] = None


class AdditionalInfo(BaseModel):
    """Model for additional information."""

    type: str = Field(..., min_length=1)
    value: str = Field(..., min_length=1)
    start: Optional[datetime] = None
    end: Optional[datetime] = None


class StaffMember(BaseModel):
    """Model for staff members."""

    username: str
    role: Role


class CafeBase(BaseModel):
    """Base model for cafes."""

    name: str = Field(..., min_length=1, max_length=50)
    slug: Optional[str] = None
    previous_slugs: Optional[List[str]] = []
    features: List[Feature]
    description: str = Field(..., min_length=1, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=755)
    image_url: Optional[str] = Field(None, max_length=755)
    affiliation: Affiliation
    is_open: bool = False
    status_message: Optional[str] = Field(None, max_length=50)
    opening_hours: List[DayHours]
    location: Location
    contact: Contact
    social_media: SocialMedia
    payment_methods: List[PaymentMethod]
    additional_info: List[AdditionalInfo]
    staff: List[StaffMember]


class Cafe(Document, CafeBase):
    """Cafe document model."""

    menu_categories: List[MenuCategory] = []

    def __init__(self, **data):
        """Initialize cafe document."""
        super().__init__(**data)
        self.slug = slugify(self.name)

    async def is_slug_unique(self, slug: str) -> bool:
        """Check if slug is unique."""
        existing_cafe = await Cafe.find_one(
            {
                "$and": [
                    {"$or": [{"slug": slug}, {"previous_slugs": slug}]},
                    {"_id": {"$ne": self.id}},
                ]
            }
        )
        return existing_cafe is None

    async def check_slug(self):
        """Check and update slug."""
        new_slug = slugify(self.name)
        if self.slug != new_slug:
            if not await self.is_slug_unique(new_slug):
                raise ValueError(f"The slug '{new_slug}' is already in use.")
            if self.slug:
                self.previous_slugs.append(self.slug)
            self.slug = new_slug

    async def check_for_duplicate_entries(self):
        """Check for duplicate payment methods and additional info."""
        # Unique PaymentMethod methods
        payment_methods_set = set()
        for pm_data in self.payment_methods:
            if isinstance(pm_data, dict):
                pm = PaymentMethod(**pm_data)
            else:
                pm = pm_data
            payment_methods_set.add(pm.method)

        if len(payment_methods_set) != len(self.payment_methods):
            raise ValueError("Duplicate PaymentMethod method detected.")

        # Unique AdditionalInfo type-value combinations
        additional_info_combinations = set()
        for info_data in self.additional_info:
            if isinstance(info_data, dict):
                info = AdditionalInfo(**info_data)
            else:
                info = info_data
            additional_info_combinations.add((info.type, info.value))

        if len(additional_info_combinations) != len(self.additional_info):
            raise ValueError(
                "Duplicate AdditionalInfo type-value combination detected."
            )

    async def check_for_duplicate_hours(self):
        """Check for duplicate hours."""
        for day_hours_data in self.opening_hours:
            day_hours = (
                DayHours(**day_hours_data)
                if isinstance(day_hours_data, dict)
                else day_hours_data
            )
            time_blocks = day_hours.blocks
            for i, block in enumerate(time_blocks):
                for other_block in time_blocks[i + 1 :]:
                    if time_blocks_overlap(block, other_block):
                        raise ValueError(
                            f"Overlapping time blocks detected on {day_hours.day}."
                        )

    async def handle_validation(self):
        """Handle validation."""
        await self.check_slug()
        await self.check_for_duplicate_hours()
        await self.check_for_duplicate_entries()

    async def update(self, *args, **kwargs):
        """Update cafe."""
        await self.handle_validation()
        return await super().update(*args, **kwargs)

    async def insert(self, *args, **kwargs):
        """Insert cafe."""
        await self.handle_validation()
        return await super().insert(*args, **kwargs)

    async def save(self, *args, **kwargs):
        """Save cafe."""
        await self.handle_validation()
        return await super().save(*args, **kwargs)

    class Settings:
        """Settings for cafe document."""

        name = "cafes"
        indexes = [
            IndexModel([("name", pymongo.ASCENDING)], unique=True),
            IndexModel([("slug", pymongo.ASCENDING)], unique=True),
            IndexModel([("description", pymongo.ASCENDING)]),
            IndexModel([("location.pavillon", pymongo.ASCENDING)]),
            IndexModel([("location.local", pymongo.ASCENDING)]),
            IndexModel([("staff.username", pymongo.ASCENDING)]),
            # IndexModel([("staff.username", pymongo.ASCENDING)], unique=True),
        ]


class StaffCreate(StaffMember):
    """Staff creation model."""

    pass


class StaffUpdate(BaseModel):
    """Staff update model."""

    role: Optional[str] = None


class StaffOut(StaffMember):
    """Staff output model."""

    pass


class CafeCreate(BaseModel):
    """Cafe creation model."""

    name: str = Field(..., min_length=1, max_length=50)
    features: List[Feature]
    description: str = Field(..., min_length=1, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=755)
    image_url: Optional[str] = Field(None, max_length=755)
    affiliation: Affiliation
    is_open: bool = False
    status_message: Optional[str] = Field(None, max_length=50)
    opening_hours: List[DayHours]
    location: Location
    contact: Contact
    social_media: SocialMedia
    payment_methods: List[PaymentMethod]
    additional_info: List[AdditionalInfo]
    staff: List[StaffMember]


class CafeUpdate(BaseModel):
    """Cafe update model."""

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


class CafeOut(CafeBase, Id):
    """Cafe output model."""

    pass


class CafeShortOut(BaseModel, Id):
    """Cafe short output model."""

    name: str = Field(..., min_length=1, max_length=50)
    slug: Optional[str] = None
    previous_slugs: Optional[List[str]] = []
    features: List[Feature]
    description: str = Field(..., min_length=1, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=755)
    image_url: Optional[str] = Field(None, max_length=755)
    affiliation: Affiliation
    is_open: bool = False
    status_message: Optional[str] = Field(None, max_length=50)
    opening_hours: List[DayHours]
    location: Location
    payment_methods: List[PaymentMethod]
    additional_info: List[AdditionalInfo]


class CafeView(View, CafeBase, IdAlias):
    """Cafe view."""

    menu: List[MenuView]

    class Settings:
        """Settings for cafe view."""

        name: str = "cafes_with_menu"
        source = "cafes"
        pipeline = [
            # Lookup all menu items for this cafe
            {
                "$lookup": {
                    "from": "menus",
                    "localField": "_id",
                    "foreignField": "cafe_id",
                    "as": "menu_items",
                }
            },
            # Reshape the categories with their items
            {
                "$addFields": {
                    "menu": {
                        "$map": {
                            "input": "$menu_categories",
                            "as": "cat",
                            "in": {
                                "_id": "$$cat._id",
                                "category": "$$cat.name",
                                "description": "$$cat.description",
                                "items": {
                                    "$map": {
                                        "input": {
                                            "$filter": {
                                                "input": "$menu_items",
                                                "as": "item",
                                                "cond": {
                                                    "$eq": [
                                                        "$$item.category_id",
                                                        "$$cat._id",
                                                    ]
                                                },
                                            }
                                        },
                                        "as": "item",
                                        "in": {
                                            "_id": "$$item._id",
                                            "name": "$$item.name",
                                            "description": "$$item.description",
                                            "tags": "$$item.tags",
                                            "image_url": "$$item.image_url",
                                            "price": "$$item.price",
                                            "in_stock": "$$item.in_stock",
                                            "options": "$$item.options",
                                        },
                                    }
                                },
                            },
                        }
                    }
                }
            },
            # Clean up temporary fields
            {"$unset": ["menu_items", "menu_categories"]},
        ]


class CafeViewOut(CafeBase, Id):
    """Cafe view output model."""

    menu: List[MenuViewOut]
