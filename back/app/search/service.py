"""
Module for handling search-related operations.
"""

import unicodedata
from typing import Any, Dict, List

from app.cafe.models import Cafe


async def normalize_query(query: str) -> str:
    """Remove diacritics from the query."""
    return "".join(
        c
        for c in unicodedata.normalize("NFD", query)
        if unicodedata.category(c) != "Mn"
    )


async def search(query: str, **filters) -> Dict[str, List[Any]]:
    """Search for cafes and menu items based on the provided query."""
    normalized_query = await normalize_query(query)
    regex_pattern = {"$regex": normalized_query, "$options": "i"}

    for key in ["is_open", "in_stock"]:
        if key in filters:
            if filters[key].lower() == "true":
                filters[key] = True
            elif filters[key].lower() == "false":
                filters[key] = False

    # Combining the search for cafes by their name and by menu items
    combined_query = {
        "$or": [
            {"name": regex_pattern},
            {"menu_items": {"$elemMatch": {"name": regex_pattern}}},
            {"menu_items": {"$elemMatch": {"tags": regex_pattern}}},
        ]
    }
    combined_query.update(filters)
    matching_cafes_full = await Cafe.find(combined_query).to_list()

    matching_cafes_and_items = []
    for cafe in matching_cafes_full:
        filtered_menu_items = [
            item
            for item in cafe.menu_items
            if normalized_query.lower() in item.name.lower()
            or any(normalized_query.lower() in tag.lower() for tag in item.tags)
        ]

        cafe_dict = {
            "_id": str(cafe.id),
            "cafe_id": str(cafe.cafe_id),
            "name": cafe.name,
            "slug": cafe.slug,
            "description": cafe.description,
            "logo_url": cafe.logo_url,
            "image_url": cafe.image_url,
            "affiliation": cafe.affiliation,
            "is_open": cafe.is_open,
            "status_message": cafe.status_message,
            "opening_hours": cafe.opening_hours,
            "location": cafe.location,
            "contact": cafe.contact,
            "social_media": cafe.social_media,
            "payment_methods": cafe.payment_methods,
            "additional_info": cafe.additional_info,
            "menu_items": filtered_menu_items,
        }
        matching_cafes_and_items.append(cafe_dict)

    return matching_cafes_and_items
