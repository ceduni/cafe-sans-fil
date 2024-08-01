from typing import List, Dict, Optional
from uuid import UUID, uuid4
from beanie import Document, DecimalAnnotation, Indexed
from pydantic import field_validator, BaseModel, Field
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

class Feature(str, Enum):
    ORDER = "Order"

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
    platform_name: str = Field(..., min_length=1, description="Name of the social media platform.")
    link: str = Field(..., min_length=1, description="Link to the social media profile.")

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

class MenuItemOption(BaseModel):
    type: str = Field(..., min_length=1, description="Type of the menu item option.")
    value: str = Field(..., min_length=1, description="Value or description of the option.")
    fee: DecimalAnnotation = Field(..., description="Additional fee for this option, if applicable.")

    @field_validator('fee')
    @classmethod
    def validate_fee(cls, fee):
        if fee < DecimalAnnotation(0.0):
            raise ValueError("Fee must be a non-negative value.")
        return fee

class NutritionInfo(BaseModel):
    calories: Optional[DecimalAnnotation] = Field(None, description="Calories in the item.")
    lipids: Optional[DecimalAnnotation] = Field(None, description="Lipid content in the item.")
    proteins: Optional[DecimalAnnotation] = Field(None, description="Protein content in the item.")
    carbohydrates: Optional[DecimalAnnotation] = Field(None, description="Carbohydrate content in the item.")
    sugar: Optional[DecimalAnnotation] = Field(None, description="Sugar content in the item.")
    sodium: Optional[DecimalAnnotation] = Field(None, description="Salt content in the item.")
    fiber: Optional[DecimalAnnotation] = Field(None, description="Fiber content in the item.")
    saturated_fat: Optional[DecimalAnnotation] = Field(None, description="Saturated fat content in the item.")
    # vitamins: Optional[DecimalAnnotation] = Field(None, description="Vitamins content in the item.")
    #percentage_fruit_vegetables_nuts: Optional[DecimalAnnotation] = Field(None, description="Percentage on fruits, vegetables and nuts in the item.")
    zinc: Optional[DecimalAnnotation] = Field(None, description="Zinc content in the item.")
    iron: Optional[DecimalAnnotation] = Field(None, description="Iron content in the item.")
    calcium: Optional[DecimalAnnotation] = Field(None, description="Calcium content in the item.")
    magnesium: Optional[DecimalAnnotation] = Field(None, description="Magnesium content in the item.")
    potassium: Optional[DecimalAnnotation] = Field(None, description="Potassium content in the item.")
    vitamina: Optional[DecimalAnnotation] = Field(None, description="VitaminA content in the item.")
    vitaminc: Optional[DecimalAnnotation] = Field(None, description="vitaminC content in the item.")
    vitamind: Optional[DecimalAnnotation] = Field(None, description="vitaminD content in the item.")
    vitamine: Optional[DecimalAnnotation] = Field(None, description="vitaminE content in the item.")
    vitamink: Optional[DecimalAnnotation] = Field(None, description="vitaminK content in the item.")
    vitaminb6: Optional[DecimalAnnotation] = Field(None, description="vitaminB6 content in the item.")
    vitaminb12: Optional[DecimalAnnotation] = Field(None, description="vitaminB12 content in the item.")

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
    ingredients: List[str] = Field(..., description="List of ingredients used in the item.")
    #diets: List[str] = Field(..., description="List of diets in which the food is eaten.")
    #allergens: List[str] = Field(..., description="List of allergens contained in the item.")
    likes: List[str] = Field(..., description="List containing the ids of the users that liked this item.")
    barecode: str = Field(None, description="Food's barecode.")
    nutritional_informations: NutritionInfo = Field(..., description="Dictionnary of the nutritive values of an item.")
    cluster: str = Field(default="unclustered", description="Item cluster.")
    health_score: float = Field(default=0, description="Item health score.")


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
    previous_slugs: List[str] = []
    features: List[Feature]
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
    health_score: float = Field(default=0, description="Cafe health score.")
    
    def __init__(self, **data):
        super().__init__(**data)
        self.slug = slugify(self.name)

    async def is_slug_unique(self, slug: str) -> bool:
        existing_cafe = await Cafe.find_one(
            {"$and": [
                {"$or": [{"slug": slug}, {"previous_slugs": slug}]},
                {"cafe_id": {"$ne": self.cafe_id}}
            ]}
        )
        return existing_cafe is None
    
    async def check_for_duplicate_entries(self):
        # Unique SocialMedia platform_name-link combinations
        social_media_combinations = set()
        for sm_data in self.social_media:
            if isinstance(sm_data, dict):
                sm = SocialMedia(**sm_data)
            else:
                sm = sm_data

            social_media_combinations.add((sm.platform_name, sm.link))

        if len(social_media_combinations) != len(self.social_media):
            raise ValueError("Duplicate SocialMedia entries detected.")

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

        # Unique MenuItem names
        menu_item_names = {item.name for item in self.menu_items}
        if len(menu_item_names) != len(self.menu_items):
            raise ValueError("Duplicate MenuItem name detected.")
        
        # Unique MenuItemOption for each MenuItem
        for item in self.menu_items:
            if isinstance(item, dict):
                options = item.get("options", [])
            else:
                options = item.options

            option_combinations = set()
            for opt in options:
                if isinstance(opt, dict):
                    opt_type = opt.get("type")
                    opt_value = opt.get("value")
                else:
                    opt_type = opt.type
                    opt_value = opt.value
                option_combinations.add((opt_type, opt_value))

            if len(option_combinations) != len(options):
                item_name = item.get("name") if isinstance(item, dict) else item.name
                raise ValueError(f"Duplicate MenuItemOption detected in item: {item_name}")

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
        name = "cafes"

def slugify(text):
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    slug = re.sub(r'\W+', '-', text)
    slug = slug.strip('-')
    return slug
