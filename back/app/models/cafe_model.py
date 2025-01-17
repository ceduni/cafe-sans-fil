from typing import List, Optional
from uuid import UUID, uuid4
from beanie import Document, View, DecimalAnnotation, Indexed
from pydantic import field_validator, BaseModel, Field
from enum import Enum
from datetime import datetime
from app.models.menu_model import MenuItemEmbedded
import re
import unicodedata

class Feature(str, Enum):
    ORDER = "Order"

class Affiliation(BaseModel):
    university: str = Field(..., min_length=1, description="Name of the university.")
    faculty: str = Field(..., min_length=1, description="Name of the faculty.")

class TimeBlock(BaseModel):
    start: str = Field(..., min_length=1, description="Start time in HH:mm format.")
    end: str = Field(..., min_length=1, description="End time in HH:mm format.")

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

class Geometry(BaseModel):
    type: str = Field(..., min_length=1, description="Type of the geometry.")
    coordinates: List[float] = Field(..., min_length=1, description="List of coordinates.")

class Location(BaseModel):
    pavillon: Indexed(str) = Field(..., min_length=1, description="Name or identifier of the pavilion.")
    local: Indexed(str) = Field(..., min_length=1, description="Local identifier within the pavilion.")
    geometry: Optional[Geometry] = Field(None, description="Geographical coordinates of the location.")

class Contact(BaseModel):
    email: Optional[str] = Field(None, description="Contact email address.")
    phone_number: Optional[str] = Field(None, description="Contact phone number.")
    website: Optional[str] = Field(None, description="Website URL.")

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is None or v == "":
            return None
        email_regex = re.compile(r'^\w+[\w.-]*@\w+[\w.-]+\.\w+$')
        if not email_regex.match(v):
            raise ValueError('Invalid email address')
        return v

class SocialMedia(BaseModel):
    facebook: Optional[str] = Field(None, description="Facebook URL.")
    instagram: Optional[str] = Field(None, description="Instagram URL.")
    x: Optional[str] = Field(None, description="X URL.")

class PaymentMethod(BaseModel):
    method: str = Field(..., min_length=1, description="Payment method used in the cafe.")
    minimum: Optional[DecimalAnnotation] = Field(None, description="Minimum amount required for this payment method, if any.")

class AdditionalInfo(BaseModel):
    type: str = Field(..., min_length=1, description="Type of additional information, e.g., 'promo', 'event'.")
    value: str = Field(..., min_length=1, description="Description or value of the additional information.")
    start: Optional[datetime] = Field(None, description="Start time or date of the additional information.")
    end: Optional[datetime] = Field(None, description="End time or date of the additional information.")

class Role(str, Enum):
    VOLUNTEER = "Bénévole"
    ADMIN = "Admin"

class StaffMember(BaseModel):
    username: Indexed(str, unique=True) = Field(..., description="Username of the staff member.")
    role: Role = Field(..., description="Role of the staff member, e.g., 'Bénévole', 'Admin'.")

class Cafe(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
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
    menu_item_ids: List[UUID]

    def __init__(self, **data):
        super().__init__(**data)
        self.slug = slugify(self.name)

    async def is_slug_unique(self, slug: str) -> bool:
        existing_cafe = await Cafe.find_one(
            {"$and": [
                {"$or": [{"slug": slug}, {"previous_slugs": slug}]},
                {"_id": {"$ne": self.id}}
            ]}
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
            raise ValueError("Duplicate AdditionalInfo type-value combination detected.")

    async def check_for_duplicate_hours(self):
        for day_hours_data in self.opening_hours:
            day_hours = DayHours(**day_hours_data) if isinstance(day_hours_data, dict) else day_hours_data

            time_blocks = day_hours.blocks
            for i, block in enumerate(time_blocks):
                for other_block in time_blocks[i+1:]:
                    if self.time_blocks_overlap(block, other_block):
                        raise ValueError(f"Overlapping time blocks detected on {day_hours.day}.")

    @staticmethod
    def time_blocks_overlap(block1, block2):
        start1, end1 = datetime.strptime(block1.start, '%H:%M'), datetime.strptime(block1.end, '%H:%M')
        start2, end2 = datetime.strptime(block2.start, '%H:%M'), datetime.strptime(block2.end, '%H:%M')
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
        # Beanie configuration
        name = "cafes"
        
    class Config:
        # Pydantic configuration
        populate_by_name = True

class CafeView(View):
    id: UUID = Field(default_factory=uuid4, alias="_id")
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
            {
                "$set": {
                    "menu_items": "$menu_items"
                }
            },
            {
                "$unset": "menu_item_ids"  # Remove the old `menu_item_ids` field
            }
        ]



def slugify(text):
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    slug = re.sub(r'\W+', '-', text)
    slug = slug.strip('-')
    return slug
