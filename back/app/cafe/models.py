"""
Module for handling cafe-related models.
"""

from datetime import datetime
from typing import List, Optional

import pymongo
from beanie import DecimalAnnotation, Insert, PydanticObjectId, Save, before_event
from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator
from pymongo import IndexModel
from slugify import slugify

from app.cafe.enums import Days, Feature, PaymentMethod
from app.cafe.menu.enums import Layout
from app.cafe.menu.models import Menu, MenuOut
from app.cafe.staff.models import Staff, StaffOut
from app.models import CustomDocument, Id
from app.user.models import UserOut


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
    floor: Optional[str] = Field(None, min_length=1)
    geometry: Optional[Geometry] = None


class Contact(BaseModel):
    """Model for contact information."""

    email: Optional[EmailStr] = Field(None, examples=["s9i2j@example.com"])
    phone_number: Optional[str] = None
    website: Optional[HttpUrl] = None


class SocialMedia(BaseModel):
    """Model for social media links."""

    facebook: Optional[HttpUrl] = None
    instagram: Optional[HttpUrl] = None
    x: Optional[HttpUrl] = None


class PaymentDetails(BaseModel):
    """Model for payment details."""

    method: PaymentMethod
    minimum: Optional[DecimalAnnotation] = None


class CafeBase(BaseModel):
    """Base model for cafes."""

    name: str = Field(..., min_length=1, max_length=50)
    slug: Optional[str] = None
    previous_slugs: Optional[List[str]] = []
    features: List[Feature] = []
    description: str = Field(..., min_length=1, max_length=255)
    logo_url: Optional[HttpUrl] = None
    banner_url: Optional[HttpUrl] = None
    photo_urls: Optional[List[HttpUrl]] = []
    affiliation: Affiliation
    is_open: bool = False
    status_message: Optional[str] = Field(None, max_length=50)
    opening_hours: List[DayHours] = []
    location: Location
    contact: Contact
    social_media: SocialMedia
    payment_details: List[PaymentDetails] = []

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


class Cafe(CustomDocument, CafeBase):
    """Cafe document model."""

    owner_id: PydanticObjectId
    staff: Staff = Staff(admin_ids=[], volunteer_ids=[])
    menu: Menu = Menu(categories=[], layout=Layout.LIST)

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
    features: List[Feature] = []
    description: str = Field(..., min_length=1, max_length=255)
    logo_url: Optional[HttpUrl] = None
    banner_url: Optional[HttpUrl] = None
    photo_urls: Optional[List[HttpUrl]] = []
    affiliation: Affiliation
    is_open: bool = False
    status_message: Optional[str] = Field(None, max_length=50)
    opening_hours: List[DayHours] = []
    location: Location
    contact: Contact
    social_media: SocialMedia
    payment_details: List[PaymentDetails] = []


class CafeUpdate(BaseModel):
    """Cafe update model."""

    name: Optional[str] = Field(None, min_length=1, max_length=50)
    features: Optional[List[Feature]] = None
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    logo_url: Optional[HttpUrl] = None
    banner_url: Optional[HttpUrl] = None
    photo_urls: Optional[List[HttpUrl]] = []
    affiliation: Optional[Affiliation] = None
    is_open: Optional[bool] = None
    status_message: Optional[str] = Field(None, max_length=50)
    opening_hours: Optional[List[DayHours]] = None
    location: Optional[Location] = None
    contact: Optional[Contact] = None
    social_media: Optional[SocialMedia] = None
    payment_details: Optional[List[PaymentDetails]] = None
    owner_id: Optional[PydanticObjectId] = None


class CafeOut(CafeBase, Id):
    """Cafe output model."""

    owner_id: PydanticObjectId


class CafeShortOut(BaseModel, Id):
    """Cafe short output model."""

    name: str = Field(..., min_length=1, max_length=50)
    slug: Optional[str] = None
    previous_slugs: Optional[List[str]] = []
    features: List[Feature]
    description: str = Field(..., min_length=1, max_length=255)
    logo_url: Optional[HttpUrl] = None
    banner_url: Optional[HttpUrl] = None
    photo_urls: Optional[List[HttpUrl]] = []
    affiliation: Affiliation
    is_open: bool = False
    status_message: Optional[str] = Field(None, max_length=50)
    opening_hours: List[DayHours]
    location: Location
    payment_details: List[PaymentDetails]


class CafeAggregateOut(CafeBase, Id):
    """Cafe aggregate output model."""

    owner: UserOut
    staff: StaffOut
    menu: MenuOut
