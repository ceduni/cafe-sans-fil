"""
Module for handling cafe-related models.
"""

import re
from datetime import datetime
from typing import List, Optional

import pymongo
from beanie import DecimalAnnotation, Insert, Save, View, before_event
from pydantic import BaseModel, Field, field_validator
from pymongo import IndexModel
from slugify import slugify

from app.cafe.enums import Days, Feature, PaymentMethod, Role
from app.cafe.menu.models import Menu, MenuView, MenuViewOut
from app.cafe.staff.models import Staff, StaffView, StaffViewOut
from app.models import CustomDocument, Id, IdAlias


class Affiliation(BaseModel):
    """Model for university affiliation."""

    university: str = Field(..., min_length=1)
    faculty: str = Field(..., min_length=1)


class TimeBlock(BaseModel):
    """Model for time blocks."""

    start: str = Field(..., min_length=1, examples=["08:00"])
    end: str = Field(..., min_length=1, examples=["12:00"])

    @field_validator("start", "end")
    @classmethod
    def validate_time_format(cls, time_value):
        """Validate time format."""
        try:
            datetime.strptime(time_value, "%H:%M")
        except ValueError:
            raise ValueError("Must be in HH:mm format.")
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

    email: Optional[str] = Field(None, examples=["s9i2j@example.com"])
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


class PaymentDetails(BaseModel):
    """Model for payment details."""

    method: PaymentMethod
    minimum: Optional[DecimalAnnotation] = None


class AdditionalInfo(BaseModel):
    """Model for additional information."""

    type: str = Field(..., min_length=1)
    value: str = Field(..., min_length=1)
    start: Optional[datetime] = None
    end: Optional[datetime] = None


class CafeBase(BaseModel):
    """Base model for cafes."""

    name: str = Field(..., min_length=1, max_length=50)
    slug: Optional[str] = None
    previous_slugs: Optional[List[str]] = []
    features: List[Feature] = []
    description: str = Field(..., min_length=1, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=755)
    image_url: Optional[str] = Field(None, max_length=755)
    affiliation: Affiliation
    is_open: bool = False
    status_message: Optional[str] = Field(None, max_length=50)
    opening_hours: List[DayHours] = []
    location: Location
    contact: Contact
    social_media: SocialMedia
    payment_details: List[PaymentDetails] = []
    additional_info: List[AdditionalInfo] = []

    @field_validator("opening_hours")
    @classmethod
    def validate_opening_hours(cls, opening_hours):
        """Validate that there are no overlapping time blocks."""

        def time_blocks_overlap(block1: TimeBlock, block2: TimeBlock):
            """Check if two time blocks overlap."""
            start1, end1 = datetime.strptime(block1.start, "%H:%M"), datetime.strptime(
                block1.end, "%H:%M"
            )
            start2, end2 = datetime.strptime(block2.start, "%H:%M"), datetime.strptime(
                block2.end, "%H:%M"
            )
            return start1 < end2 and start2 < end1

        day_blocks: dict[str, List[TimeBlock]] = {}

        for day_hours_data in opening_hours:
            day_hours = (
                DayHours(**day_hours_data)
                if isinstance(day_hours_data, dict)
                else day_hours_data
            )
            if day_hours.day not in day_blocks:
                day_blocks[day_hours.day] = []
            day_blocks[day_hours.day].extend(day_hours.blocks)

        for day, blocks in day_blocks.items():
            for i, block in enumerate(blocks):
                for other_block in blocks[i + 1 :]:
                    if time_blocks_overlap(block, other_block):
                        raise ValueError(f"Overlapping time blocks detected on {day}.")
        return opening_hours

    @field_validator("payment_details")
    @classmethod
    def validate_payment_details(cls, payment_details):
        """Validate that payment methods are unique."""
        payment_details_set = set()
        for pm_data in payment_details:
            if isinstance(pm_data, dict):
                pm = PaymentDetails(**pm_data)
            else:
                pm = pm_data
            payment_details_set.add(pm.method)

        if len(payment_details_set) != len(payment_details):
            raise ValueError("Duplicate payment method detected.")
        return payment_details

    @field_validator("additional_info")
    @classmethod
    def validate_additional_info(cls, additional_info):
        """Validate that additional info entries are unique."""
        additional_info_combinations = set()
        for info_data in additional_info:
            if isinstance(info_data, dict):
                info = AdditionalInfo(**info_data)
            else:
                info = info_data
            additional_info_combinations.add((info.type, info.value))

        if len(additional_info_combinations) != len(additional_info):
            raise ValueError(
                "Duplicate AdditionalInfo type-value combination detected."
            )
        return additional_info


class Cafe(CustomDocument, CafeBase):
    """Cafe document model."""

    staff: Staff = Staff(admin_ids=[], volunteer_ids=[])
    menu: Menu = Menu(categories=[])

    @before_event([Insert, Save])
    async def handle_slug(self):
        """Handle slug."""
        prev_slug = self.slug
        new_slug = slugify(self.name)

        if prev_slug != new_slug:
            if prev_slug:
                self.previous_slugs.append(prev_slug)

            while new_slug in self.previous_slugs:
                self.previous_slugs.remove(new_slug)

            await Cafe.find({"previous_slugs": new_slug}).update_many(
                {"$pull": {"previous_slugs": new_slug}}
            )

            self.slug = new_slug

    class Settings:
        """Settings for cafe document."""

        name = "cafes"
        indexes = [
            IndexModel([("name", pymongo.ASCENDING)], unique=True),
            IndexModel([("slug", pymongo.ASCENDING)], unique=True),
            IndexModel([("description", pymongo.ASCENDING)]),
            IndexModel([("location.pavillon", pymongo.ASCENDING)]),
            IndexModel([("location.local", pymongo.ASCENDING)]),
        ]


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
    payment_details: List[PaymentDetails]
    additional_info: Optional[List[AdditionalInfo]] = None


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
    payment_details: Optional[List[PaymentDetails]] = None
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
    payment_details: List[PaymentDetails]
    additional_info: List[AdditionalInfo]


class CafeView(View, CafeBase, IdAlias):
    """Cafe view with complete staff and menu data."""

    staff: StaffView
    menu: MenuView

    class Settings:
        name: str = "cafes_view"
        source = "cafes"
        pipeline = [
            # Lookup all menu items
            {
                "$lookup": {
                    "from": "menus",
                    "localField": "_id",
                    "foreignField": "cafe_id",
                    "as": "menu_items",
                }
            },
            # Lookup admin user
            {
                "$lookup": {
                    "from": "users",
                    "localField": "staff.admin_ids",
                    "foreignField": "_id",
                    "pipeline": [
                        {
                            "$project": {
                                "_id": 1,
                                "username": 1,
                                "email": 1,
                                "matricule": 1,
                                "first_name": 1,
                                "last_name": 1,
                                "photo_url": 1,
                            }
                        }
                    ],
                    "as": "admins",
                }
            },
            # Lookup volunteer user
            {
                "$lookup": {
                    "from": "users",
                    "localField": "staff.volunteer_ids",
                    "foreignField": "_id",
                    "pipeline": [
                        {
                            "$project": {
                                "_id": 1,
                                "username": 1,
                                "email": 1,
                                "matricule": 1,
                                "first_name": 1,
                                "last_name": 1,
                                "photo_url": 1,
                            }
                        }
                    ],
                    "as": "volunteers",
                }
            },
            # Reshape both menu and staff
            {
                "$addFields": {
                    "menu": {
                        "categories": {
                            "$concatArrays": [
                                # Group items with no category
                                [
                                    {
                                        # "_id": None, # Prevent generate ID
                                        "name": None,
                                        "description": None,
                                        "items": {
                                            "$map": {
                                                "input": {
                                                    "$filter": {
                                                        "input": "$menu_items",
                                                        "as": "item",
                                                        "cond": {
                                                            "$eq": [
                                                                "$$item.category_id",
                                                                None,
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
                                    }
                                ],
                                # Group items with categories
                                {
                                    "$map": {
                                        "input": "$menu.categories",
                                        "as": "cat",
                                        "in": {
                                            "_id": "$$cat._id",
                                            "name": "$$cat.name",
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
                                },
                            ]
                        }
                    },
                    "staff": {"admins": "$admins", "volunteers": "$volunteers"},
                }
            },
            # Clean up temporary fields
            {
                "$unset": [
                    "menu_items",
                    "admins",
                    "volunteers",
                    "staff.admin_ids",
                    "staff.volunteer_ids",
                ]
            },
        ]


class CafeViewOut(CafeBase, Id):
    """Cafe view output model."""

    staff: StaffViewOut
    menu: MenuViewOut
