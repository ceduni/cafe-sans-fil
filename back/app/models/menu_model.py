from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import field_validator, BaseModel, Field
from beanie import Document,DecimalAnnotation, Indexed
import re

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

class MenuItem(Document):
    item_id: UUID = Field(default_factory=uuid4, description="Unique identifier of the menu item.")
    name: Indexed(str, unique=True) = Field(..., description="Name of the menu item.")
    tags: List[str] = Field(..., description="List of tags associated with the menu item.")
    description: Indexed(str) = Field(..., description="Description of the menu item.")
    image_url: Optional[str] = Field(None, description="Image URL of the menu item.")
    price: DecimalAnnotation = Field(..., description="Price of the menu item.")
    in_stock: bool = Field(False, description="Availability status of the menu item.")
    category: Indexed(str) = Field(..., description="Category of the menu item.")
    options: List[MenuItemOption] = Field(..., description="List of options available for the menu item.")

    @field_validator('price')
    @classmethod
    def validate_price(cls, price):
        if price < DecimalAnnotation(0.0):
            raise ValueError("Price must be a non-negative value.")
        return price

def slugify(text):
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    slug = re.sub(r'\W+', '-', text)
    slug = slug.strip('-')
    return slug
