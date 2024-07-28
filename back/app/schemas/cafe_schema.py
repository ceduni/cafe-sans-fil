from typing import List, Dict, Optional
from uuid import UUID
from pydantic import field_validator, ConfigDict, BaseModel, Field
from datetime import datetime, timedelta
from beanie import DecimalAnnotation
from app.models.cafe_model import Feature, DayHours, Location, Contact, SocialMedia, PaymentMethod, AdditionalInfo, StaffMember, MenuItemOption, NutritionInfo

"""
This module defines the Pydantic-based schemas for cafe operations in the Café application. 
These schemas are utilized for request and response validation, serialization, 
and documentation specific to cafe listings, details, and management.

Note: These models are for API data interchange related to cafes and not direct database models.
"""

# --------------------------------------
#               Menu
# --------------------------------------

class MenuItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Name of the menu item.")
    tags: List[str] = Field(..., max_length=20, description="List of tags for the menu item.")
    description: str = Field(..., min_length=1, max_length=255, description="Description of the menu item.")
    image_url: Optional[str] = Field(None, max_length=755, description="Image URL of the menu item.")
    price: DecimalAnnotation = Field(..., description="Price of the menu item.")
    in_stock: bool = Field(..., description="Availability status of the menu item.")
    category: str = Field(..., min_length=1, max_length=50, description="Category of the menu item.")
    options: List[MenuItemOption] = Field(..., description="Options available for the menu item.")
    ingredients: List[str] = Field(..., description="List of ingredients in the menu item.")
    #diets: List[str] = Field(..., description="List of diets in which the food is eaten.")
    #allergens: List[str] = Field(..., description="List of allergens contained in the item.")
    barecode: Optional[str] = Field(None, description="Food's barecode.")
    nutritional_informations: NutritionInfo = Field(..., description="Dictionnary of the nutritive values of an item.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Cheeseburger",
            "tags": ["Rapide", "Savoureux"],
            "description": "Un délicieux cheeseburger avec laitue, tomate et fromage",
            "image_url": "https://thedelightfullaugh.com/wp-content/uploads/2020/09/smashed-double-cheeseburger.jpg",
            "price": 5.99,
            "in_stock": True,
            "category": "Burgers",
            "options": [
                {"type": "taille", "value": "grand", "fee": 0.5},
                {"type": "ingrédients", "value": "bœuf", "fee": 0},
                {"type": "ingrédients", "value": "laitue", "fee": 0},
                {"type": "ingrédients", "value": "tomate", "fee": 0},
                {"type": "ingrédients", "value": "fromage", "fee": 0}
            ],
            "ingredients": ["milk", "cheese", "bread"],
            #"diets": ["Vegetarian"],
            #"allergens": ["Peanuts", "Dairy"],
            "barecode": "123e4567-e892-12d3-a456-426614174000",
            "nutritional_information": {"calories": 300, "proteins": 25, "carbohydrates": 50, "sodium": 15}
        }
    })

    @field_validator('price')
    @classmethod
    def validate_price(cls, price):
        if price < 0:
            raise ValueError("Price must be a non-negative value.")
        return price
    
class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Updated name of the menu item.")
    tags: Optional[List[str]] = Field(None, max_length=20, description="Updated tags for the menu item.")
    description: Optional[str] = Field(None, min_length=1, max_length=255, description="Updated description of the menu item.")
    image_url: Optional[str] = Field(None, max_length=755, description="Updated image URL of the menu item.")
    price: Optional[DecimalAnnotation] = Field(None, description="Updated price of the menu item.")
    in_stock: Optional[bool] = Field(None, description="Updated availability status of the menu item.")
    category: Optional[str] = Field(None, min_length=1, max_length=50, description="Updated category of the menu item.")
    options: Optional[List[MenuItemOption]] = Field(None, description="Updated options for the menu item.")
    ingredients: Optional[List[str]] = Field(None, description="Updated list of ingredients for the menu item.")
    #diets: Optional[List[str]] = Field(None, description="Updated list of diets for the menu item.")
    #allergens: Optional[List[str]] = Field(None, description="Updated list of allergens for the menu item.")
    likes: Optional[List[str]] = Field(None, description="Updated list of likes for the menu item.")
    barecode: Optional[str] = Field(None, description="Updated barecode of the menu item.")
    nutritional_information: Optional[NutritionInfo] = Field(None, description="Updated nutritional information for the menu item.")
    cluster: Optional[str] = Field(None, description="Item cluster.")
    health_score: Optional[float] = Field(None, description="Item health score.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Cheeseburger Spécial",
            "tags": ["Gourmet", "Nouveau"],
            "description": "Cheeseburger gourmet avec bacon et sauce spéciale",
            "image_url": "https://thedelightfullaugh.com/wp-content/uploads/2020/09/smashed-double-cheeseburger.jpg",
            "price": 7.99,
            "in_stock": False,
            "category": "Burgers Spéciaux",
            "options": [
                {"type": "épice", "value": "piquant", "fee": 0.75},
                {"type": "supplément", "value": "bacon", "fee": 1.0}
            ],
            "ingredients": ["milk", "cheese", "bread"],
            #"diets": ["Vegetarian"],
            #"allergens": ["Peanuts", "Dairy"],
            "likes": ["20176472"],
            "barecode": "123e4567-e892-12d3-a456-426614174000",
            "nutritional_information": {"calories": 300, "proteins": 25, "carbohydrates": 50, "sodium": 15}
        }
    })

    #TODO: Add new fields

    @field_validator('price')
    @classmethod
    def validate_price(cls, price):
        if price < 0:
            raise ValueError("Price must be a non-negative value.")
        return price
    
class MenuItemOut(BaseModel):
    item_id: UUID = Field(..., description="Unique identifier of the menu item.")
    name: str = Field(..., description="Name of the menu item.")
    slug: str = Field(..., description="Slug of the menu item.")
    tags: List[str] = Field(..., description="Tags associated with the menu item.")
    description: str = Field(..., description="Description of the menu item.")
    image_url: Optional[str] = Field(None, description="Image URL of the menu item.")
    price: DecimalAnnotation = Field(..., description="Price of the menu item.")
    in_stock: bool = Field(..., description="Availability status of the menu item.")
    category: str = Field(..., description="Category of the menu item.")
    options: List[MenuItemOption] = Field(..., description="Options available for the menu item.")
    ingredients: List[str] = Field(..., description="Ingredients associated with the menu item.")
    #diets: List[str] = Field(..., description="Diets associated with the menu item.")
    #allergens: List[str] = Field(..., description="Allergens associated with the menu item.")
    likes: List[str] = Field(..., description="Identifier of users who like the menu item.")
    barecode: Optional[str] = Field(None, description="Barecode of the menu item.")
    nutritional_informations: NutritionInfo = Field(..., description="Nutritional information of the menu item.")
    cluster: Optional[str] = Field(None, description="Item cluster.")
    health_score: Optional[float] = Field(None, description="Item health score.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "item_id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Cheeseburger",
            "slug": "cheeseburger",
            "tags": ["Classique", "Fromage"],
            "description": "Un cheeseburger classique avec une tranche de fromage fondant",
            "image_url": "https://thedelightfullaugh.com/wp-content/uploads/2020/09/smashed-double-cheeseburger.jpg",
            "price": 5.99,
            "in_stock": True,
            "category": "Burgers",
            "options": [
                {"type": "taille", "value": "moyen", "fee": 0.0},
                {"type": "sans oignon", "value": "oui", "fee": 0.0}
            ],
            "ingredients": ["milk", "cheese", "bread"],
            #"diets": ["Vegetarian"],
            #"allergens": ["Peanuts", "Dairy"],
            "likes": ["20176472"],
            "barecode": "123e4567-e892-12d3-a456-426614174000",
            "nutritional_information": {"calories": 300, "proteins": 25, "carbohydrates": 50, "sodium": 15},
            "cluster": "0",
            "health_score": 0.0
        }
    })

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
    image_url: Optional[str] = Field(None, max_length=755, description="Image URL of the cafe.")
    faculty: str = Field(..., min_length=1, max_length=100, description="Faculty associated with the cafe.")
    is_open: bool = Field(..., description="Indicates if the cafe is currently open.")
    status_message: Optional[str] = Field(None, max_length=50, description="Status message about the cafe.")
    opening_hours: List[DayHours] = Field(..., description="Opening hours of the cafe.")
    location: Location = Field(..., description="Location details of the cafe.")
    contact: Contact = Field(..., description="Contact information of the cafe.")
    social_media: List[SocialMedia] = Field(..., description="Social media profiles of the cafe.")
    payment_methods: List[PaymentMethod] = Field(..., description="Accepted payment methods at the cafe.")
    additional_info: List[AdditionalInfo] = Field(..., description="Additional information about the cafe.")
    staff: List[StaffMember] = Field(..., description="Staff members of the cafe.")
    menu_items: List[MenuItemCreate] = Field(..., description="Menu items offered by the cafe.")
    health_score: Optional[float] = Field(None, description="Health score of the cafe.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Café Central",
            "features": ["Order"],
            "description": "Un café populaire près de la bibliothèque principale.",
            "image_url": "https://media.architecturaldigest.com/photos/5b083c4675a4f940de3da8f1/master/pass/case-study-coffee.jpg",
            "faculty": "Science",
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
            "social_media": [{"platform_name": "Facebook", "link": "http://fb.com/centralcafe"}],
            "payment_methods": [{"method": "Carte de Crédit", "minimum": 4.0}],
            "staff": [
                {"username": "cafesansfil", "role": "Admin"}
            ],
            "menu_items": [
                {
                    "name": "Cheeseburger",
                    "tags": ["Rapide", "Savoureux"],
                    "description": "Un délicieux cheeseburger avec laitue, tomate et fromage",
                    "image_url": "https://thedelightfullaugh.com/wp-content/uploads/2020/09/smashed-double-cheeseburger.jpg",
                    "price": 5.99,
                    "in_stock": True,
                    "category": "Burgers",
                    "options": [
                        {"type": "taille", "value": "grand", "fee": 0.5},
                        {"type": "ingrédients", "value": "bœuf", "fee": 0},
                        {"type": "ingrédients", "value": "laitue", "fee": 0},
                        {"type": "ingrédients", "value": "tomate", "fee": 0},
                        {"type": "ingrédients", "value": "fromage", "fee": 0}
                    ],
                    "ingredients": ["milk", "cheese", "bread"],
                    "nutritional_information": {"calories": 300, "proteins": 25, "carbohydrates": 50, "sodium": 15},
                },
                {
                    "name": "Chicken Caesar Salad",
                    "tags": ["Léger", "Fraîcheur"],
                    "description": "Une salade César avec du poulet grillé, de la laitue romaine et de la vinaigrette César",
                    "image_url": None,
                    "price": 7.99,
                    "in_stock": False,
                    "category": "Salads",
                    "options": [],
                    "ingredients": ["milk", "cheese", "bread"],
                    "nutritional_information": {"calories": 300, "proteins": 25, "carbohydrates": 50, "sodium": 15},
                }
            ],
            "health_score": 4.5,
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
    image_url: Optional[str] = Field(None, max_length=755, description="Updated image URL of the cafe.")
    faculty: Optional[str] = Field(None, min_length=1, max_length=100, description="Updated faculty association of the cafe.")
    is_open: Optional[bool] = Field(None, description="Updated open status of the cafe.")
    status_message: Optional[str] = Field(None, max_length=50, description="Updated status message of the cafe.")
    opening_hours: Optional[List[DayHours]] = Field(None, description="Updated opening hours of the cafe.")
    location: Optional[Location] = Field(None, description="Updated location details of the cafe.")
    contact: Optional[Contact] = Field(None, description="Updated contact information of the cafe.")
    social_media: Optional[List[SocialMedia]] = Field(None, description="Updated social media profiles of the cafe.")
    payment_methods: Optional[List[PaymentMethod]] = Field(None, description="Updated payment methods accepted at the cafe.")
    additional_info: Optional[List[AdditionalInfo]] = Field(None, description="Updated additional information about the cafe.")
    health_score : Optional[float] = Field(None, description="Updated health score of the cafe.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Café Central",
            "features": ["Order"],
            "description": "Un café populaire près de la bibliothèque principale.",
            "image_url": "https://media.architecturaldigest.com/photos/5b083c4675a4f940de3da8f1/master/pass/case-study-coffee.jpg",
            "faculty": "Science",
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
            "social_media": [{"platform_name": "Facebook", "link": "http://fb.com/centralcafe"}],
            "payment_methods": [{"method": "Carte de Crédit", "minimum": 4.0}],
            "additional_info": [
                {
                    "type": "promo",
                    "value": "10% de réduction les lundis",
                    "start": datetime.now() - timedelta(hours=5),
                    "end": datetime.now() + timedelta(minutes=30)
                }
            ],
            "health_score": 0.8
        }
    })

class CafeOut(BaseModel):
    cafe_id: UUID = Field(..., description="Unique identifier of the cafe.")
    name: str = Field(..., description="Name of the cafe.")
    slug: str = Field(..., description="Slug of the cafe.")
    previous_slugs: List[str] = Field(None, description="Previous slugs of the cafe.")
    features: List[Feature] = Field(..., description="Features of the cafe.")
    description: str = Field(..., description="Description of the cafe.")
    image_url: Optional[str] = Field(None, description="Image URL of the cafe.")
    faculty: str = Field(..., description="Faculty associated with the cafe.")
    is_open: bool = Field(..., description="Open status of the cafe.")
    status_message: Optional[str] = Field(None, description="Status message about the cafe.")
    opening_hours: List[DayHours] = Field(..., description="Opening hours of the cafe.")
    location: Location = Field(..., description="Location details of the cafe.")
    contact: Contact = Field(..., description="Contact information of the cafe.")
    social_media: List[SocialMedia] = Field(..., description="Social media profiles of the cafe.")
    payment_methods: List[PaymentMethod] = Field(..., description="Payment methods accepted at the cafe.")
    additional_info: List[AdditionalInfo] = Field(..., description="Additional information about the cafe.")
    staff: List[StaffMember] = Field(..., description="Staff members of the cafe.")
    menu_items: List[MenuItemOut] = Field(..., description="Menu items offered by the cafe.")
    health_score : float = Field(..., description="Health score of the cafe.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "cafe_id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Café Central",
            "slug": "cafe-central",
            "previous_slugs": ["cafe-central-1", "cafe-central-2"],
            "features": ["Order"],
            "description": "Un café populaire près de la bibliothèque principale.",
            "image_url": "https://media.architecturaldigest.com/photos/5b083c4675a4f940de3da8f1/master/pass/case-study-coffee.jpg",
            "faculty": "Science",
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
            "social_media": [{"platform_name": "Facebook", "link": "http://fb.com/centralcafe"}],
            "payment_methods": [{"method": "Carte de Crédit", "minimum": 4.0}],
            "staff": [
                {"username": "johndoe", "role": "Admin"},
                {"username": "janedoe", "role": "Admin"},
                {"username": "johndoe2", "role": "Bénévole"},
                {"username": "janedoe2", "role": "Bénévole"},
                {"username": "johndoe3", "role": "Bénévole"},
                {"username": "janedoe3", "role": "Bénévole"}
            ],
            "menu_items": [
                {
                    "item_id": "123e4567-e89b-12d3-a456-426614174001",
                    "name": "Cheeseburger",
                    "slug": "cheeseburger",
                    "tags": ["Rapide", "Savoureux"],
                    "description": "Un délicieux cheeseburger avec laitue, tomate et fromage",
                    "image_url": "https://thedelightfullaugh.com/wp-content/uploads/2020/09/smashed-double-cheeseburger.jpg",
                    "price": 5.99,
                    "in_stock": True,
                    "category": "Burgers",
                    "options": [
                        {"type": "taille", "value": "grand", "fee": 0.5},
                        {"type": "ingrédients", "value": "bœuf", "fee": 0},
                        {"type": "ingrédients", "value": "laitue", "fee": 0},
                        {"type": "ingrédients", "value": "tomate", "fee": 0},
                        {"type": "ingrédients", "value": "fromage", "fee": 0}
                    ],
                    "ingredients": ["milk", "cheese", "bread"],
                    "nutritional_information": {"calories": 300, "proteins": 25, "carbohydrates": 50, "sodium": 15},
                },
                {
                    "item_id": "123e4567-e89b-12d3-a456-426614174002",
                    "name": "Chicken Caesar Salad",
                    "slug": "chicken-caesar-salad",
                    "tags": ["Léger", "Fraîcheur"],
                    "description": "Une salade César avec du poulet grillé, de la laitue romaine et de la vinaigrette César",
                    "image_url": None,
                    "price": 7.99,
                    "in_stock": False,
                    "category": "Salads",
                    "options": [],
                    "ingredients": ["milk", "cheese", "bread"],
                    "nutritional_information": {"calories": 300, "proteins": 25, "carbohydrates": 50, "sodium": 15},
                }
            ],
            "health_score": 8.5,
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
    image_url: Optional[str] = Field(None, description="Image URL of the cafe.")
    faculty: str = Field(..., description="Faculty associated with the cafe.")
    is_open: bool = Field(..., description="Open status of the cafe.")
    status_message: Optional[str] = Field(None, description="Status message about the cafe.")
    opening_hours: List[DayHours] = Field(..., description="Opening hours of the cafe.")
    location: Location = Field(..., description="Location details of the cafe.")
    payment_methods: List[PaymentMethod] = Field(..., description="Payment methods accepted at the cafe.")
    additional_info: List[AdditionalInfo] = Field(..., description="Additional information about the cafe.")
    health_score: float = Field(..., description="Health score of the cafe.")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "cafe_id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Café Central",
            "slug": "cafe-central",
            "previous_slugs": ["cafe-central-1", "cafe-central-2"],
            "features": ["Order"],
            "description": "Un café populaire près de la bibliothèque principale.",
            "image_url": "https://media.architecturaldigest.com/photos/5b083c4675a4f940de3da8f1/master/pass/case-study-coffee.jpg",
            "faculty": "Science",
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
            ],
            "health_score": 8.5
        }
    })

