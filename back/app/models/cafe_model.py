import re
import unicodedata
from datetime import datetime
from enum import Enum
from typing import List, Optional

from beanie import DecimalAnnotation, Document, Indexed, PydanticObjectId, View
from pydantic import BaseModel, Field, field_validator

from app.models.menu_model import MenuItemEmbedded


class Feature(str, Enum):
    ORDER = "Order"


class Affiliation(BaseModel):
    university: str = Field(..., min_length=1)
    faculty: str = Field(..., min_length=1)


class TimeBlock(BaseModel):
    start: str = Field(..., min_length=1)
    end: str = Field(..., min_length=1)

    @field_validator("start", "end")
    @classmethod
    def validate_time_format(cls, time_value):
        try:
            datetime.strptime(time_value, "%H:%M")
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
    day: Days
    blocks: List[TimeBlock]


class Geometry(BaseModel):
    type: str = Field(..., min_length=1)
    coordinates: List[float] = Field(..., min_length=1)


class Location(BaseModel):
    pavillon: Indexed(str) = Field(..., min_length=1)
    local: Indexed(str) = Field(..., min_length=1)
    geometry: Optional[Geometry] = None


class Contact(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    website: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v is None or v == "":
            return None
        email_regex = re.compile(r"^\w+[\w.-]*@\w+[\w.-]+\.\w+$")
        if not email_regex.match(v):
            raise ValueError("Invalid email address")
        return v


class SocialMedia(BaseModel):
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    x: Optional[str] = None


class PaymentMethod(BaseModel):
    method: str = Field(..., min_length=1)
    minimum: Optional[DecimalAnnotation] = None


class AdditionalInfo(BaseModel):
    type: str = Field(..., min_length=1)
    value: str = Field(..., min_length=1)
    start: Optional[datetime] = None
    end: Optional[datetime] = None


class Role(str, Enum):
    VOLUNTEER = "Bénévole"
    ADMIN = "Admin"


class StaffMember(BaseModel):
    username: Indexed(str, unique=True)
    role: Role


class Cafe(Document):
    name: Indexed(str, unique=True)
    slug: Indexed(str, unique=True) = None
    previous_slugs: List[str] = []
    features: List[Feature]
    description: Indexed(str)
    logo_url: Optional[str] = None
    image_url: Optional[str] = None
    affiliation: Affiliation
    is_open: bool = False
    status_message: Optional[str] = None
    opening_hours: List[DayHours]
    location: Location
    contact: Contact
    social_media: SocialMedia
    payment_methods: List[PaymentMethod]
    additional_info: List[AdditionalInfo]
    staff: List[StaffMember]
    menu_item_ids: List[PydanticObjectId]

    def __init__(self, **data):
        super().__init__(**data)
        self.slug = slugify(self.name)

    async def is_slug_unique(self, slug: str) -> bool:
        existing_cafe = await Cafe.find_one(
            {
                "$and": [
                    {"$or": [{"slug": slug}, {"previous_slugs": slug}]},
                    {"_id": {"$ne": self.id}},
                ]
            }
        )
        return existing_cafe is None

    async def check_for_duplicate_entries(self):
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
                # Convert dict to AdditionalInfo instance
                info = AdditionalInfo(**info_data)
            else:
                info = info_data

            additional_info_combinations.add((info.type, info.value))

        if len(additional_info_combinations) != len(self.additional_info):
            raise ValueError(
                "Duplicate AdditionalInfo type-value combination detected."
            )

    async def check_for_duplicate_hours(self):
        for day_hours_data in self.opening_hours:
            day_hours = (
                DayHours(**day_hours_data)
                if isinstance(day_hours_data, dict)
                else day_hours_data
            )

            time_blocks = day_hours.blocks
            for i, block in enumerate(time_blocks):
                for other_block in time_blocks[i + 1 :]:
                    if self.time_blocks_overlap(block, other_block):
                        raise ValueError(
                            f"Overlapping time blocks detected on {day_hours.day}."
                        )

    @staticmethod
    def time_blocks_overlap(block1, block2):
        start1, end1 = datetime.strptime(block1.start, "%H:%M"), datetime.strptime(
            block1.end, "%H:%M"
        )
        start2, end2 = datetime.strptime(block2.start, "%H:%M"), datetime.strptime(
            block2.end, "%H:%M"
        )
        return start1 < end2 and start2 < end1

    async def update(self, *args, **kwargs):
        new_slug = slugify(self.name)
        if self.slug != new_slug:
            if not await self.is_slug_unique(new_slug):
                raise ValueError(f"The slug '{new_slug}' is already in use.")
            if self.slug:
                self.previous_slugs.append(self.slug)
            self.slug = new_slug
        await self.check_for_duplicate_hours()
        await self.check_for_duplicate_entries()
        return await super().update(*args, **kwargs)

    async def insert(self, *args, **kwargs):
        new_slug = slugify(self.name)
        if self.slug != new_slug:
            if not await self.is_slug_unique(new_slug):
                raise ValueError(f"The slug '{new_slug}' is already in use.")
            if self.slug:
                self.previous_slugs.append(self.slug)
            self.slug = new_slug
        await self.check_for_duplicate_hours()
        await self.check_for_duplicate_entries()
        return await super().insert(*args, **kwargs)

    async def save(self, *args, **kwargs):
        new_slug = slugify(self.name)
        if self.slug != new_slug:
            if not await self.is_slug_unique(new_slug):
                raise ValueError(f"The slug '{new_slug}' is already in use.")
            if self.slug:
                self.previous_slugs.append(self.slug)
            self.slug = new_slug
        await self.check_for_duplicate_hours()
        await self.check_for_duplicate_entries()
        return await super().save(*args, **kwargs)

    class Settings:
        name = "cafes"


class CafeView(View):
    id: PydanticObjectId = Field(..., alias="_id")
    name: Indexed(str, unique=True)
    slug: Indexed(str, unique=True) = None
    previous_slugs: List[str] = []
    features: List[Feature]
    description: Indexed(str)
    logo_url: Optional[str] = None
    image_url: Optional[str] = None
    affiliation: Affiliation
    is_open: bool = False
    status_message: Optional[str] = None
    opening_hours: List[DayHours]
    location: Location
    contact: Contact
    social_media: SocialMedia
    payment_methods: List[PaymentMethod]
    additional_info: List[AdditionalInfo]
    staff: List[StaffMember]
    menu_items: List[MenuItemEmbedded]

    class Settings:
        name: str = "cafe_with_menu"
        source = "cafes"
        pipeline = [
            {
                "$lookup": {
                    "from": "menus",
                    "localField": "_id",
                    "foreignField": "cafe_id",
                    "as": "menu_items",
                    "pipeline": [
                        {
                            "$project": {
                                "_id": 1,
                                "name": 1,
                                "description": 1,
                                "image_url": 1,
                                "price": 1,
                                "in_stock": 1,
                                "category": 1,
                                "options": 1,
                            }
                        }
                    ],
                }
            },
            {"$set": {"menu_items": "$menu_items"}},
            {"$unset": "menu_item_ids"},  # Remove the old `menu_item_ids` field
        ]


def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    slug = re.sub(r"\W+", "-", text)
    slug = slug.strip("-")
    return slug
