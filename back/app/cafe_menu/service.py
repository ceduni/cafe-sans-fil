"""
Module for handling menu-related operations.
"""

from typing import List

from beanie import PydanticObjectId

from app.cafe.models import Cafe
from app.cafe_menu.models import (
    MenuCategory,
    MenuCategoryCreate,
    MenuCategoryOut,
    MenuCategoryUpdate,
    MenuItem,
    MenuItemCreate,
    MenuItemUpdate,
)


class MenuService:
    """Service class for CRUD and search operations on Menu."""

    @staticmethod
    async def create_category(cafe: Cafe, data: MenuCategoryCreate) -> MenuCategoryOut:
        """Create a new menu category for a cafe."""
        new_category = MenuCategory(**data.model_dump())
        cafe.menu_categories.append(new_category)
        await cafe.save()
        return MenuCategoryOut(**new_category.model_dump())

    @staticmethod
    async def update_category(
        cafe: Cafe,
        id: PydanticObjectId,
        data: MenuCategoryUpdate,
    ) -> MenuCategoryOut:
        """Update a menu category for a cafe."""
        for idx, category in enumerate(cafe.menu_categories):
            if category.id == id:
                updated_data = category.model_dump() | data.model_dump(
                    exclude_unset=True
                )
                cafe.menu_categories[idx] = MenuCategory(**updated_data)
                await cafe.save()
                return MenuCategoryOut(**cafe.menu_categories[idx].model_dump())

        raise ValueError("Category not found")

    @staticmethod
    async def delete_category(cafe: Cafe, id: PydanticObjectId) -> None:
        """Delete a menu category for a cafe."""
        original_len = len(cafe.menu_categories)
        cafe.menu_categories = [c for c in cafe.menu_categories if c.id != id]

        if len(cafe.menu_categories) == original_len:
            raise ValueError("Category not found")

        await cafe.save()

    @staticmethod
    async def get_items(**filters: dict):
        """Get menu items."""
        sort_by = filters.pop("sort_by", "name")
        return MenuItem.find(filters).sort(sort_by)

    @staticmethod
    async def get_item(item_id: PydanticObjectId) -> MenuItem:
        """Get a menu item by ID."""
        return await MenuItem.find_one({"_id": item_id})

    @staticmethod
    async def create_item(cafe: Cafe, data: MenuItemCreate) -> MenuItem:
        """Create a new menu item for a cafe."""
        item = MenuItem(**data.model_dump(), cafe_id=cafe.id)
        await item.insert()
        return item

    @staticmethod
    async def update_item(item: MenuItem, data: MenuItemUpdate) -> MenuItem:
        """Update a menu item."""
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        await item.save()
        return item

    @staticmethod
    async def delete_item(item: MenuItem) -> None:
        """Delete a menu item."""
        await item.delete()

    @staticmethod
    async def create_many_categories(
        cafe: Cafe, data: List[MenuCategoryCreate]
    ) -> List[MenuCategory]:
        """Create multiple menu categories for a cafe."""
        for category_data in data:
            new_category = MenuCategory(**category_data.model_dump())
            cafe.menu_categories.append(new_category)
        await cafe.save()
        return cafe.menu_categories

    @staticmethod
    async def create_many_items(
        cafe: Cafe, data: List[MenuItemCreate]
    ) -> List[MenuItem]:
        """Create multiple menu items for a cafe."""
        items = [
            MenuItem(**item_data.model_dump(), cafe_id=cafe.id) for item_data in data
        ]
        await MenuItem.insert_many(items)
        return items

    @staticmethod
    async def update_many_items(
        item_ids: List[PydanticObjectId], data: MenuItemUpdate
    ) -> List[MenuItem]:
        """Update multiple menu items."""
        result = await MenuItem.find_many({"_id": {"$in": item_ids}}).update_many(
            {"$set": data.model_dump(exclude_unset=True)}
        )
        if result.matched_count == 0:
            raise ValueError("No menu items found for the provided IDs")

        return await MenuItem.find_many({"_id": {"$in": item_ids}}).to_list()

    @staticmethod
    async def delete_many_items(item_ids: List[PydanticObjectId]) -> None:
        """Delete multiple menu items."""
        await MenuItem.find_many({"_id": {"$in": item_ids}}).delete_many()
